BUCKET_REGION = "ap-east-1"

DESTINATION = "S3://maai6-data-bkt/hk_tradable_stocks/"

BASE_URL = "https://www3.hkexnews.hk/{}"

END_PT = "sdw/search/searchsdw.aspx"

HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
    " like Gecko) Chrome/108.0.0.0 Safari/537.36"
}

STOCK_LIST_END_PT = "sdw/search/stocklist.aspx"

STOCK_PAYLOAD = "?sortby=stockcode&shareholdingdate={yyyymmdd}"

PAYLOAD_TEMPLATE = {
    "__EVENTTARGET": "btnSearch",
    "__EVENTARGUMENT": "",
    "__VIEWSTATE": "",
    "__VIEWSTATEGENERATOR": "",
    "today": "",
    "sortBy": "shareholding",
    "sortDirection": "desc",
    "alertMsg": "",
    "txtShareholdingDate": "",
    "txtStockCode": "",
    "txtStockName": "",
    "txtParticipantID": "",
    "txtParticipantName": "",
}
