# https://pypi.org/project/airtable/
from dateutil.parser import parse
from itertools import count
import requests
import json
import csv
import os

def run():
    """
    Function must be named 'run' so that django's 'runscript' command will work.
    Example command: ./manage.py runscript scrapers.arhscraper

    This function scrapes two websites for their funding/grants.
    """

    GRANTS_GOV_KEYWORDS = [
        'Algeria',
        'MENA',
        'Middle East and Northern Africa',
    ]

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
    master_list = []

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
            'Closed Date': close_date,
            'Link': f"https://www.grants.gov/web/grants/view-opportunity.html?oppId={record['id']}",
            'Source': 'Grants.gov'
        }

        #add grant.gov scrapped data into the master_list
        master_list.append(data)


    #**************************************************************************************************
    #European Scrapper that adds to the master_list
    EUROPEAN_COMMISION_KEYWORDS = [
        'Algeria',
        'MENA'
    ]

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

    json_response = json.loads(response.text)
    distinct_results = {}
    for result in json_response['results']:
        if result['content'] != '' and result['content'] not in distinct_results:
            distinct_results[result['content']] = result

    for result,data in distinct_results.items():
        master_hits.append(data)

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
            'Link': f"https://ec.europa.eu/info/funding-tenders/opportunities/portal/screen/opportunities/topic/{record['metadata']['identifier'][0].lower()}",
            'Source': 'Eurpean Commission'
        }

        #add data collected from the European Script to the master_list
        master_list.append(data)

    # ----------------------------
    # Export data into a CSV file.
    funds_csv = open("scrapers/funds.csv", 'w')
    # Use python's csv package to turn our list of dictionaries into rows in a csv file.
    csv_writer = csv.DictWriter(funds_csv, fieldnames=list(master_list[0].keys())) # ASSUMPTION: the master_list will have at least one entry
    # Create the header row using the fieldnames set in the line above.
    csv_writer.writeheader()
    # Create our rows.
    csv_writer.writerows(master_list)
    # Close file.
    funds_csv.close()
