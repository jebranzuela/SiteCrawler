import sys
from datetime import datetime

import requests
from bs4 import BeautifulSoup


start = datetime.now()
print(start)

sys.setrecursionlimit(50000000)
print(sys.getrecursionlimit())

osau_urls = []
ext_urls = {}
counter = 0

def scrapeSite(url):
	global osau_urls
	global ext_urls
	global counter

	# Request site here
	r = requests.get(url)
	html = r.content

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
		if link[0:21] == "http://localhost/osau":
			osau_temp.append(link)
		else:
			if link not in list(ext_urls.keys()):
				ext_urls[link] = url

	# Check if links are already in urls[]
	# in_ext = set(ext_urls)
	# in_temp = set(ext_temp)
	# diff = in_temp - in_ext
	# ext_urls = ext_urls + list(diff)

	in_osau = set(osau_urls)
	in_temp = set(osau_temp)
	diff = in_temp - in_osau
	osau_urls = osau_urls + list(diff)

	
	file = open("sites.txt", "w")

	# Write all links to sites.txt
	for link in osau_urls:
		file.writelines("%s\n" % link)

	file.write("==========EXTERNAL LINKS==========\n")

	for link in ext_urls:
		file.writelines("%s,%s\n" % (link, ext_urls[link]))

	file.close()

	# Pass all new links to method
	for url in diff:
		scrapeSite(url)

		# if counter == 10:
		# 	return 0
		# else:
	# 	counter += 1
			
url = "http://localhost/osau"
scrapeSite(url)

# file = open("sites.txt", "w")

# # Write all links to sites.txt
# for link in osau_urls:
# 	file.writelines("%s\n" % link)

# file.write("==========EXTERNAL LINKS==========\n")

# for link in ext_urls:
# 	file.writelines("%s\n" % link)

#file.close()

end = datetime.now()
print(end)