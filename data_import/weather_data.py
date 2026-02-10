import pandas as pd

from typing import Optional

def get_weather_data(
        start_year: int = 2021, 
        end_year: int = 2026,
        save_path: Optional[str] = None
        ) -> pd.DataFrame:
    try:
        if save_path != None:
            df = pd.read_csv(save_path, low_memory=False)
            df["Tid(norsk normaltid)"] = pd.to_datetime(df["Tid(norsk normaltid)"], utc=True).dt.tz_convert('Europe/Oslo')
            return df
    except:
        pass
    
    # read and combine the year files
    yearly_data = []
    for year in range(start_year, end_year):
        df = pd.read_csv(
            f"./data/{year}.csv",
            sep=";",
            parse_dates=["Tid(norsk normaltid)"],
            dayfirst=True
        )
        yearly_data.append(df)
    data: pd.DataFrame = pd.concat(yearly_data, ignore_index=True)
    
    # fix the types and such
    numeric_cols = [
        "Nedbør (1 t)",
        "Lufttemperatur",
        "Lufttrykk i stasjonsnivå",
        "Vindretning",
        "Middelvind",
    ]
    for col in numeric_cols:
        data[col] = data[col].astype(str).str.replace(",", ".") # read csv doesnt handle comma decimals well :(
        data[col] = pd.to_numeric(data[col], errors="coerce", downcast="float") # some values are set to -, which probably means they're missing?
    data = data.dropna(subset=numeric_cols)

    if save_path != None:
        data.to_csv(save_path)

    return data