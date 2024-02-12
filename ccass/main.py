import requests
from datetime import datetime
import pandas as pd
import logging
import pytz
import sys
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_result
from ccass import BASE_URL, STOCK_PAYLOAD, STOCK_LIST_END_PT, HEADERS, DESTINATION, BUCKET_REGION
from utils import Storage, DEFAULT_LOGGING_FORMAT


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format=DEFAULT_LOGGING_FORMAT)


@retry(
    stop=stop_after_attempt(3),  # try 3 times
    wait=wait_fixed(2),  # wait 2 seconds before retry
    retry=retry_if_result(lambda x: x is None),  # if return None, retry
    retry_error_callback=lambda x: None,  # return None after all retry
)
def fetch_stock_list(dt: datetime) -> pd.DataFrame:
    url = BASE_URL.format(STOCK_LIST_END_PT) + STOCK_PAYLOAD.format(
        yyyymmdd=dt.strftime("%Y%m%d")
    )
    with requests.get(url, timeout=5, headers=HEADERS) as resp:
        if resp.status_code == 200:
            try:
                data = resp.json()
                df = pd.DataFrame.from_dict(data)
                return df
            except Exception as ex:
                logger.error(f"Status 200 but {ex} - {sys.exc_info()}")
        else:
            logger.error(f"Status: {resp.status_code}")
    return


def run():
    df = fetch_stock_list(datetime.now(tz=pytz.timezone("Asia/Hong_Kong")))
    storage = Storage(full_path=DESTINATION, region_name=BUCKET_REGION)
    storage.save_df(df, "test.csv")
    return


if __name__ == "__main__":
    run()
