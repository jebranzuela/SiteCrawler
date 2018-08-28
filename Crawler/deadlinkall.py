import requests
from datetime import datetime
from bs4 import BeautifulSoup

start = datetime.now()
print(start)

osau_urls = []
external_urls = []

def scrapeSite(url):
	
	# Request site here
	r = requests.get(url)
	html = r.content

	# Parse HTML to get all href
	soup = BeautifulSoup(html, 'html.parser')
	links = soup.find_all('a')
	urls = [link.get('href') for link in links
    if link.get('href') and (link.get('href')[0:4]=='http' or link.get('href')[0:4]=='https')]
	
	# Sort links if internal or external
	results = []
	for url in enumerate(urls,1):
	    try:
	        r = requests.get(url)
	        report = str(r.status_code)
	        if r.history:
	            history_status_codes = [str(h.status_code) for h in r.history]
	            report += ' [HISTORY: ' + ', '.join(history_status_codes) + ']'
	            result = (r.status_code, r.history, url, 'No error. Redirect to ' + r.url)
	        elif r.status_code >= 200 and r.status_code <= 230:
	            result = (r.status_code, r.history, url, 'No error. No redirect.')
	        else:
	            result = (r.status_code, r.history, url, 'Error?')
	    except Exception as e:
	        result = (0, [], url, e)
	        
	    results.append(result)

	# Check if links are already in urls[]
	# Pass all new links to method

	# for url in diff:
	# 	scrapeSite(url)


url = "https://localhost/osau"

end = datetime.now()
print(end)