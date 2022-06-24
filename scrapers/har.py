import requests

s = requests.Session()

KEYWORD = "Algeria"

r = s.post(
    "https://www.grants.gov/grantsws/rest/opportunities/search/",
    headers={
        "Accept": "application/json, text/javascript, */*; q=0.01"
    },
    data='{"startRecordNum":0,"keyword":"'+KEYWORD+'","oppNum":"","cfda":"","oppStatuses":"forecasted|posted"}',
)


print(r.text)