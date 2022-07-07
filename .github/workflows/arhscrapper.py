import requests
from airtable import airtable
# https://pypi.org/project/airtable/
import json

AIRTABLE_API_KEY = 'key77vbawxykDygId'
AIRTABLE_BASE_ID = 'appyLuakMhHhy0IpY'
AIRTABLE_TABLE_NAME = 'Grants.gov'

GRANTS_GOV_KEYWORDS = [
    'Algeria',
    'MENA'
]

airtable_api = airtable.Airtable(AIRTABLE_BASE_ID, AIRTABLE_API_KEY)


# START POPULTAING LIST

# keep track of what page number we're on
current_page = 1

# each page has 25 results, starting with index: 0.
# this means results 0-24 are on the first page, the second page has results 25-49, and so on
start_record_num = ((current_page - 1) * 25)
keyword_phrase = '%2C%20'.join(GRANTS_GOV_KEYWORDS)
post_data = '{"startRecordNum":"'+str(start_record_num)+'","keyword":"'+keyword_phrase+'","oppNum":"","cfda":"","oppStatuses":"forecasted|posted"}'

# DON'T CHANGE THE FOLLOWING LINES:
post_url = 'https://www.grants.gov/grantsws/rest/opportunities/search/'
headers = {
    'Content-Type': 'application/json; charset=utf-8',
}

# master list that'll hold all of the results
master_hits = []

# make the first response.  This will give us results, AND how many results total to expect
response = requests.post(post_url, headers=headers, data=post_data)

# convert it to JSON
json_response = json.loads(response.text)

# grab the total hit count -- this is what we'll use to tell when we've gathered all of the results
total_hits = json_response['hitCount']

# grab the first page of results and add them to our master hits list
master_hits.extend(json_response['oppHits'])

# record how many hits we've ingested so far
total_hits_ingested = len(json_response['oppHits'])

# continue to loop through pages until we've gathered all of the hits there are in our search results
while len(master_hits) < int(total_hits):
    # increment the current page and recalculate the starting record
    current_page += 1
    start_record = ((current_page - 1) * 25)
    # update the post data to hold the new "starting record" number
    post_data = '{"startRecordNum":"'+str(start_record)+'","keyword":"'+keyword_phrase+'","oppNum":"","cfda":"","oppStatuses":"forecasted|posted"}'
    # ...and make a new post request
    response = requests.post(post_url, headers=headers, data=post_data)
    json_response = json.loads(response.text)
    # add these into the master list
    master_hits.extend(json_response['oppHits'])

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
    if record['openDate'] != '':
        open_date = record['openDate'].replace(' ', '')
    close_date = None
    if record['closeDate'] != '':
        close_date = record['closeDate'].replace(' ', '')
    
    # data: assemble! :mjolnir:
    data = {
        'Title': record['title'],
        'Posted Date': open_date,
        'Close Date': close_date,
        'Link': f"https://www.grants.gov/web/grants/view-opportunity.html?oppId={record['id']}"
    }
    # create the record
    airtable_api.create(AIRTABLE_TABLE_NAME, data)
#Footer
