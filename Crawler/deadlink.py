# System modules
import sys
from datetime import datetime

# Third-party modules. Need to install first
import requests
from bs4 import BeautifulSoup

# Print when the script started
start = datetime.now()
print(start)

# Increase recursion limit to prevent errors
sys.setrecursionlimit(50000000)
print(sys.getrecursionlimit())

# Filter to remove social media sharer links
SHARER = ['share.php', 'share?url', 'sharer.php']
# Filter to remove questions and school search
SKIP  = ['http://localhost/osau/questions', 'http://localhost/osau/search/school?loc=', 'http://localhost/osau/search/school?specialization=', 'http://localhost/osau/search/school?ranking=', 'http://localhost/osau/search/school?type=', 'http://localhost/osau/search/school?categ=']

osau_urls = []
ext_urls = {}
error_urls = []
counter = 0

def skipLinks(link):
	# Check if string contains substring in list SKIP
	global SKIP

	for i in SKIP:
		if i in link:
			return 0
	
	return 1

def notShare(link):
	# Check if string contains substring in list SHARER
	global SHARER

	for i in SHARER:
		if i in link:
			return 0
	return 1

def scrapeSite(url):
	# Main method for crawling the website
	global osau_urls
	global ext_urls
	global error_urls
	global counter
	global SHARER 
	global skip

	try:
		# Request site here
		r = requests.get(url)
		html = r.content

		# Write the following data in a text file:
		# 1. Link currently parsed
		# 2. Total number of OSAU links parsed
		# 3. Total number of external links parsed
		file = open("output.txt", 'a')
		file.write("Parsing: " + url + "\n")
		file.write("No. of OSAU links: " + str(len(osau_urls)) + "\n")
		file.write("No. of External links: " + str(len(ext_urls)) + "\n")
		file.close()

		# Parse HTML to get all href
		soup = BeautifulSoup(html, 'html.parser')
		links = soup.find_all('a')
		urls = [link.get('href') for link in links if link.get('href') and (link.get('href')[0:4]=='http' or link.get('href')[0:5]=='https')]
		
		# Sort links if internal or external
		osau_temp = []
		ext_temp = []
		for link in urls:
			if link[0:21] == "http://localhost/osau" and skipLinks(link):
				osau_temp.append(link)

			elif skipLinks(link):
				if link not in list(ext_urls.keys()) and notShare(link):
					ext_urls[link] = url

		# Check if links are already in list to aavoid duplicates
		in_osau = set(osau_urls)
		in_temp = set(osau_temp)
		diff = in_temp - in_osau
		osau_urls = osau_urls + list(diff)

		# Pass all new links to method
		for url in diff:
			scrapeSite(url)

	# Catch exception to prevent script from stopping when an error occurs
	except Exception as e:
		error_urls.append(url)
		print(e)
		print('\n'+ url)
			
url = "http://localhost/osau"
scrapeSite(url)

# Write all links to sites.txt

file = open("sites.txt", "w")
for link in osau_urls:
	file.writelines("%s\n" % link)

file.write("==========EXTERNAL LINKS==========\n")

for link in ext_urls:
	file.writelines("%s,%s\n" % (link,ext_urls[link]))

file.write("==========ERROR==========\n")

for link in error_urls:
	file.writelines("%s\n" % link)

file.close()

file = open("external.csv", "w")

for link in ext_urls:
	file.writelines("%s,%s\n" % (link,ext_urls[link]))

file.close()
# ============== End write ===============

# Print when the script ends
end = datetime.now()
print(end)