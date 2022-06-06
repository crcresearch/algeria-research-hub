import json
import requests


post_data = '{"startRecordNum":"0","keyword":"Algeria","oppNum":"","cfda":"","oppStatuses":"forecasted|posted"}'

post_url = 'https://www.grants.gov/grantsws/rest/opportunities/search/'
headers = {
    'Content-Type': 'application/json; charset=utf-8',
}

# Master list
master_hits = []

# Extracting list (links)
response = requests.post(post_url, headers=headers, data=post_data)

json_response = json.loads(response.text)

total_hits = json_response['hitcount']

first_page = json_response['oppHits']

print(total_hits)
print(len(first_page))

# print(json_response)

# total_hits_ingested = len(first_page)

# while total_hits_ingested < total_hits:
#     current_page += 1
#     next_round = current_page = (25)
    # make new call with updated post_date to change 'startthecordNum' = next round (26)
# END POPULATING LIST

# push master_list up to airtables

