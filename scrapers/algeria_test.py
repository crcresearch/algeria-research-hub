import requests
import json

post_data = '{"startRecordNum":"0","keyword":"Algeria","oppNum":"","cfda":"","oppStatuses":"forecasted|posted"}'

post_url = 'https://www.grants.gov/grantsws/rest/opportunities/search/'
headers = {
    'Content-Type': 'application/json; charset=utf-8',
}

# master list
master_hits = []

# START POPULTAING LIST
response = requests.post(post_url, headers=headers, data=post_data)

json_response = json.loads(response.text)

total_hits = json_response['hitCount']

first_page = json_response['oppHits']

print(total_hits)
print(len(first_page))

total_hits_ingested = len(first_page)
current_page = 1

while total_hits_ingested < total_hits:
    current_page += 1
    # make new call with updated post_data to change `startRecordNum` = next round (26)

# END POPULATING LIST

# push master_list up to airtable
#   https://airtable.com/api

