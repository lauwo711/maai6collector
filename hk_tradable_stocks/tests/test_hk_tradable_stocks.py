import pandas as pd

from hk_tradable_stocks.main import fetch_stock_list
import requests
from datetime import datetime
import pytz
from unittest.mock import patch


class MockResponse(requests.Response):
    def __init__(self, json_data, status_code):
        super().__init__()
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data

    def close(self):
        return


def test_fetch_stock_list():
    mock_json = [
        {"c": "00001", "n": "CK HUTCHISON HOLDINGS LIMITED"},
        {"c": "00002", "n": "CLP HOLDINGS LIMITED"},
    ]
    mock_resp = MockResponse(mock_json, 200)
    exp_res = pd.DataFrame(data=mock_json)
    with patch.object(requests, "get", return_value=mock_resp):
        res = fetch_stock_list(datetime.now(tz=pytz.timezone("Asia/Hong_Kong")))
    assert res.equals(exp_res)


def test_storage_validity():
    from hk_tradable_stocks import DESTINATION, BUCKET_REGION
    assert len(BUCKET_REGION.split("-")) == 3
    assert DESTINATION.startswith("S3://")


@patch.object(target=requests, attribute="get")
def test_fetch_stock_list_using_patch_decorator(mock_req_get):
    mock_json = [
        {"c": "00001", "n": "CK HUTCHISON HOLDINGS LIMITED"},
        {"c": "00002", "n": "CLP HOLDINGS LIMITED"},
    ]
    mock_req_get.return_value = MockResponse(mock_json, 200)
    exp_res = pd.DataFrame(data=mock_json)
    res = fetch_stock_list(dt=datetime.now(tz=pytz.timezone("Asia/Hong_Kong")))
    assert res.equals(exp_res)
