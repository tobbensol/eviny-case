import requests
import pandas as pd

from typing import Optional
from datetime import datetime, timedelta


def get_consumption_data(area: str, 
                         start_year: int = 2021, 
                         end_year: int = 2026,
                         save_path: Optional[str] = None
                         ) -> pd.DataFrame:
    
    try:
        if save_path != None:
            df = pd.read_csv(save_path, low_memory=False)
            df["startTime"] = pd.to_datetime(df["startTime"], utc=True).dt.tz_convert('Europe/Oslo')
            return df
    except:
        pass

    api_link = "https://api.elhub.no/energy-data/v0/price-areas"
    start_time = datetime(year=start_year, month=1, day=1)
    end_time = datetime(year=end_year, month=1, day=1)

    result = []
    while start_time < end_time:
        # API only allows for time intervals of max 1 month.
        temp_end = min(start_time + timedelta(weeks=4), end_time)

        params = {
            "dataset": "CONSUMPTION_PER_GROUP_MBA_HOUR",
            "startDate": f"{start_time.isoformat()}+02:00",
            "endDate": f"{temp_end.isoformat()}+02:00",
        }

        response = requests.get(f"{api_link}/{area}", params=params)
        response.raise_for_status()

        result.extend(response.json()["data"][0]["attributes"]["consumptionPerGroupMbaHour"])
        start_time = temp_end
    
    consumption_df = pd.DataFrame(result)
    consumption_df["startTime"] = pd.to_datetime(consumption_df["startTime"], utc=True).dt.tz_convert('Europe/Oslo')

    if save_path != None:
        consumption_df.to_csv(save_path)

    return consumption_df