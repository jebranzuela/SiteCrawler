import requests
import csv
from datetime import datetime
from bs4 import BeautifulSoup

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

start = datetime.now()
print(start)

# Get all external links from a text file
# with open('external.txt', 'r') as f:
#     links = [line.strip() for line in f]

# reader = csv.DictReader(open('external.csv', 'rt'))
result = []
links = []

# for line in reader:
#     links.append(line)

# Get all external links from a text file
with open('external.csv', 'r') as f:
    reader = csv.reader(f)
    links = list(reader)

#headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'Accept-Encoding': 'gzip, deflate'}
# Issue a header request and check if it is success or not
# Write the result in the corresponding text file
for link in links:
    try:
        r = requests.head(link[0],headers=headers,allow_redirects=True, verify=False)
        report = str(r.status_code)

        if r.history and (r.status_code >= 200 and r.status_code <= 310):
            history_status_codes = [str(h.status_code) for h in r.history]
            report += ' [HISTORY: ' + ', '.join(history_status_codes) + ']'
            result = (r.status_code, r.history, link[0], link[1], 'No error. Redirect to ' + r.url)

            print(link[0] + ',' + link[1] + ',' + str(r.status_code), file=open("external_success.txt", "a"))
            print(r, file=open("external_success.txt", "a"))
            print(str(result) + '\n', file=open("external_success.txt", "a"))

        elif r.status_code >= 200 and r.status_code <= 310:
            result = (r.status_code, r.history, link[0], link[1], 'No error. No redirect.')

            print(link[0] + ',' + link[1] + ',' + str(r.status_code), file=open("external_success.txt", "a"))
            print(r, file=open("external_success.txt", "a"))
            print(str(result) + '\n', file=open("external_success.txt", "a"))

        else:
            result = (r.status_code, r.history, link, 'Error')
            print(link[0] + ',' + link[1] + ',' + str(r.status_code), file=open("links_with_error.txt", "a"))
            print(link[0] + ',' + link[1] + ',' + str(r.status_code), file=open("external_error.txt", "a"))
            print(r, file=open("external_error.txt", "a"))
            print(str(result) + '\n', file=open("external_error.txt", "a"))

    except Exception as e:
        result = (0, [], link, e)

        print(link[0] + ',' + link[1] + ',0', file=open("links_with_error.txt", "a"))
        print(link[0] + ',' + link[1] + ',0', file=open("external_error.txt", "a"))
        print('0', file=open("external_error.txt", "a"))
        print(str(result) + '\n', file=open("external_error.txt", "a"))

end = datetime.now()
print(end)