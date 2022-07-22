from doctest import master
import requests
from airtable import airtable
# https://pypi.org/project/airtable/
import json
from dateutil.parser import parse

AIRTABLE_API_KEY = 'key77vbawxykDygId'
AIRTABLE_BASE_ID = 'appyLuakMhHhy0IpY'
AIRTABLE_TABLE_NAME = 'European'

EUROPEAN_COMMISION_KEYWORDS = [
    'Algeria',
    'MENA'
]

airtable_api = airtable.Airtable(AIRTABLE_BASE_ID, AIRTABLE_API_KEY)

# page number
current_page = 1

start_record_num = current_page
keyword_phrase = ', '.join(EUROPEAN_COMMISION_KEYWORDS)
post_data = {
    "apiKey": "SEDIA",
    "text": keyword_phrase+"*",
    "pageSize": "1000",
    "pageNumber": "1",
}

# DON'T CHANGE THE FOLLOWING LINES:
post_url = "https://api.tech.ec.europa.eu/search-api/prod/rest/search"
headers = {
    'Content-Type': 'application/json; charset=utf-8',
}

# master list that'll hold all of the results
master_hits = []

# make the first response.  This will give us results, AND how many results total to expect
response = requests.post(
    post_url,
    headers=headers,
    params=post_data,
    data='-----------------------------280098105110154896432867507591\r\nContent-Disposition: form-data; name="query"; filename="blob"\r\nContent-Type: application/json\r\n\r\n{"bool":{"must":[{"terms":{"type":["0","1","2","8"]}},{"terms":{"status":["31094501","31094502","31094503"]}}]}}\r\n-----------------------------280098105110154896432867507591\r\nContent-Disposition: form-data; name="languages"; filename="blob"\r\nContent-Type: application/json\r\n\r\n["en"]\r\n-----------------------------280098105110154896432867507591\r\nContent-Disposition: form-data; name="sort"; filename="blob"\r\nContent-Type: application/json\r\n\r\n{"field":"sortStatus","order":"ASC"}\r\n-----------------------------280098105110154896432867507591--\r\n'
)

#print the responses
# print ("response.text: ",response.text)

# convert it to JSON (the output is xml)
json_response = json.loads(response.text)
distinct_results = {}
for result in json_response['results']:
    if result['content'] != '' and result['content'] not in distinct_results:
        distinct_results[result['content']] = result

for result,data in distinct_results.items():
    master_hits.append(data)


# grab the total hit count -- this is what we'll use to tell when we've gathered all of the results
#total_hits = json_response['hitCount']

# grab the first page of results and add them to our master hits list
#master_hits.extend(json_response['oppHits'])

# record how many hits we've ingested so far
#total_hits_ingested = len(json_response['oppHits'])

#print ('hitcount',total_hits)
#print ('masterHits', master_hits)
#print ('totalHitsIngested', total_hits_ingested)

# continue to loop through pages until we've gathered all of the hits there are in our search results
#while len(master_hits) < int(total_hits):
    # increment the current page and recalculate the starting record
    #current_page += 1
    #start_record = ((current_page - 1) * 25)
    # update the post data to hold the new "starting record" number
    #post_data = '{"startRecordNum":"'+str(start_record)+'","keyword":"'+keyword_phrase+'","oppNum":"","cfda":"","oppStatuses":"forecasted|posted"}'
    # ...and make a new post request
    #response = requests.post(post_url, headers=headers, data=post_data)
    #json_response = json.loads(response.text)
    # add these into the master list
   # master_hits.extend(json_response['oppHits'])

# at this point, our master hits list SHOULD be the same length as the number of total hits, which means we've collected all there is.

# END POPULATING LIST
# ----------------------------
# BEGIN UPDATING AIRTABLE

# clear the entire table
data = airtable_api.get(AIRTABLE_TABLE_NAME)
for table_record in data['records']:
    # a table record looks like: OrderedDict([('id', 'recmZ3JFwTsUcJWSo'), ('createdTime', '2022-06-14T12:47:39.000Z'), ('fields', OrderedDict([('Posted Date', '2022-06-01'), ('Title', 'Title 2'), ('Close Date', '2022-06-23'), ('Link', 'https://www.google.com')]))])
    # just delete it, it'll get re-added if it's in our fetch above
    airtable_api.delete(AIRTABLE_TABLE_NAME, table_record['id'])

# now load all of our records into the table
for record in master_hits:
    # for open date and close date, some of them are empty strings (not sure why?)
    # so we need to pass in a `None` value rather than the empty string as Airtables can't parse an empty string as a date
    open_date = None
    if record['metadata']['startDate'] != '':
        open_date = record['metadata']['startDate'][0]
        open_date = parse(open_date).strftime('%Y-%m-%d')
    close_date = None
    if 'deadlineDate' in record['metadata'] and len(record['metadata']['deadlineDate']) > 0:
        close_date = record['metadata']['deadlineDate'][-1]
        close_date = parse(close_date).strftime('%Y-%m-%d')
    
    # data: assemble! :mjolnir:
    data = {
        'Title': record['content'],
        'Posted Date': open_date,
        'Closed Date': close_date,
        'Link': f"https://ec.europa.eu/info/funding-tenders/opportunities/portal/screen/opportunities/topic/{record['metadata']['identifier'][0].lower()}"
    }          
    print(data)   
    # create the record
    airtable_api.create(AIRTABLE_TABLE_NAME, data)