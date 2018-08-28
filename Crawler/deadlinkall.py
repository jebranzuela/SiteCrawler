import requests
from datetime import datetime
from bs4 import BeautifulSoup

start = datetime.now()
print(start)

osau_urls = []
ext_urls = []

def scrapeSite(url):
	global osau_urls
	global ext_urls
	
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
			ext_temp.append(link)

	# Check if links are already in urls[]
	in_ext = set(ext_urls)
	in_temp = set(ext_temp)
	diff = in_temp - in_ext
	ext_urls = ext_urls + list(diff)

	in_osau = set(osau_urls)
	in_temp = set(osau_temp)
	diff = in_temp - in_osau
	osau_urls = osau_urls + list(diff)

	# Write all links to sites.txt
	file = open("sites.txt", "w")

	for link in osau_urls:
		file.writelines("%s\n" % link)

	file.write("==========EXTERNAL LINKS==========\n")

	for link in ext_urls:
		file.writelines("%s\n" % link)

	file.close()

	# Pass all new links to method
	for url in diff:
		scrapeSite(url)


url = "http://localhost/osau"
scrapeSite(url)

end = datetime.now()
print(end)