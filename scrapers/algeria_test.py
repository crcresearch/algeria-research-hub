import requests

KEYWORD = 'Algeria'

post_data = {"startRecordNum":"0","keyword":"Algeria","oppNum":"","cfda":"","oppStatuses":"forecasted|posted"}

post_url = 'https://www.grants.gov/grantsws/rest/opportunities/search/'
headers = {
    'Content-Type': 'application/json; charset=utf-8',
}
cookies = {
    'BIGipServerProd-Apache-HTTP-Pool':	"2403731978.3367.0000",
    'BIGipServerProd-Liferay-HTTPS-Pool':	"285870602.32287.0000",
    'JSESSIONID':	"BFC73C6E0CFFEB0F3B47BD1C71877EA0",
    'LFR_SESSION_STATE_5':	"1653588590997"
}

response = requests.post(post_url, data=post_data, headers=headers, cookies=cookies)

print(response.text)

