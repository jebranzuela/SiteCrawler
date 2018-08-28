import requests
from datetime import datetime
from bs4 import BeautifulSoup

start = datetime.now()
print(start)

# Get all external links from a text file
with open('external.txt', 'r') as f:
    links = [line.strip() for line in f]

result = []
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}

# Issue a header request and check if it is success or not
# Write the result in the corresponding text file
for link in links:
    try:
        r = requests.get(link,headers=headers,allow_redirects=True, verify=False)
        report = str(r.status_code)

        if r.history and (r.status_code >= 200 and r.status_code <= 310):
            history_status_codes = [str(h.status_code) for h in r.history]
            report += ' [HISTORY: ' + ', '.join(history_status_codes) + ']'
            result = (r.status_code, r.history, link, 'No error. Redirect to ' + r.url)

            print(link, file=open("external_success_2.txt", "a"))
            print(r, file=open("external_success_2.txt", "a"))
            print(str(result) + '\n', file=open("external_success_2.txt", "a"))

        elif r.status_code >= 200 and r.status_code <= 310:
            result = (r.status_code, r.history, link, 'No error. No redirect.')

            print(link, file=open("external_success.txt_2", "a"))
            print(r, file=open("external_success_2.txt", "a"))
            print(str(result) + '\n', file=open("external_success_2.txt", "a"))

        else:
            result = (r.status_code, r.history, link, 'Error')
            print(link, file=open("links_with_error_2.txt", "a"))
            print(link, file=open("external_error_2.txt", "a"))
            print(r, file=open("external_error_2.txt", "a"))
            print(str(result) + '\n', file=open("external_error_2.txt", "a"))

    except Exception as e:
        result = (0, [], link, e)

        print(link, file=open("links_with_error_2.txt", "a"))
        print(link, file=open("external_error_2.txt", "a"))
        print('0', file=open("external_error_2.txt", "a"))
        print(str(result) + '\n', file=open("external_error_2.txt", "a"))

end = datetime.now()
print(end)