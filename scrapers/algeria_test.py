import requests


post_data = '{"startRecordNum":"0","keyword":"Algeria","oppNum":"","cfda":"","oppStatuses":"forecasted|posted"}'

post_url = 'https://www.grants.gov/grantsws/rest/opportunities/search/'
headers = {
    'Content-Type': 'application/json; charset=utf-8',
}

response = requests.post(post_url, headers=headers, data=post_data)

print(response.text)

