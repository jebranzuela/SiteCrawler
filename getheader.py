import requests
from datetime import datetime
from bs4 import BeautifulSoup

start = datetime.now()
print(start)

with open('external.txt', 'r') as f:
    links = [line.strip() for line in f]

result = []
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}

for link in links:
    try:
        r = requests.head(link,headers=headers,allow_redirects=True)
        report = str(r.status_code)

        if r.history:
            history_status_codes = [str(h.status_code) for h in r.history]
            report += ' [HISTORY: ' + ', '.join(history_status_codes) + ']'
            result = (r.status_code, r.history, link, 'No error. Redirect to ' + r.url)

            print(link, file=open("external_success.txt", "a"))
            print(r, file=open("external_success.txt", "a"))
            print(str(result) + '\n', file=open("external_success.txt", "a"))

        elif r.status_code >= 200 and r.status_code <= 310:
            result = (r.status_code, r.history, link, 'No error. No redirect.')

            print(link, file=open("external_success.txt", "a"))
            print(r, file=open("external_success.txt", "a"))
            print(str(result) + '\n', file=open("external_success.txt", "a"))

        else:
            result = (r.status_code, r.history, link, 'Error')
            print(link, file=open("links_with_error.txt", "a"))
            print(link, file=open("external_error.txt", "a"))
            print(r, file=open("external_error.txt", "a"))
            print(str(result) + '\n', file=open("external_error.txt", "a"))

    except Exception as e:
        result = (0, [], link, e)

        print(link, file=open("links_with_error.txt", "a"))
        print(link, file=open("external_error.txt", "a"))
        print(r, file=open("external_error.txt", "a"))
        print(str(result) + '\n', file=open("external_error.txt", "a"))

end = datetime.now()
print(end)