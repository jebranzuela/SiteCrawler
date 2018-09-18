# Crawler Documentation

## Installing Dependencies

1. The script runs using Python 3. To install, refer to the following links:

	1. For Windows: https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-local-programming-environment-on-windows-10

	2. For Mac: https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-local-programming-environment-on-macos

2. Install requests module while in a virtual environment using `pip install requests`.

3. Install BeautifulSoup module while in a virtual environment using `pip install beautifulsoup4`.

4. Install urllib module while in a virtual environment using `pip install urllib3`

## File Structure

### 1. Crawler

	a. deadlink.py

		Input: None
		Output: external.csv
				output.txt
				sites.txt

### 2. Request Handler

	a. getheader.py
		Input: None
		Output: links_with_error.csv 
				external_error.txt
				external_success.txt
	b. getall.py
		Input: None
		Output: links_with_error_2.csv 
				external_error_2.txt
				external_success_2.txt
	c. getbrowser.py 
		Input: None
		Output: None

## How to Use

1. Go to `Documents/Scripts`.

2. Start up your virtual environment. If you are using my previous machine, do `source ScrapeEnv/bin/activate`.

3. Go to `Crawler`.

4. Run `python deadlink.py`.

5. Wait until the script finishes running.

6. Copy `external.csv` to folder `RequestHandler`.

7. Run `python getheader.py`.

8. Wait until the script finishes running.

9. Run `python getall.py`.

10. Wait until the script finishes running.

11. All links that return with an error is located in `links_with_error_2.csv`. Copy-paste the text inside to a spreadsheet program. Numbers(Mac) already separates the comma separated values to corresponding columns.

12. Some sites respond with an error if accessed using terminal scripts. To check, run `getbrowser.py`.

## In-depth Code Review


### `deadlink.py`

`deadlink.py` initially get links from the homepage of OSAU. From there, it will crawl all links and store it in a list until all links are exhausted. After crawling the links, it will store the data on a file to be used on the scripts in `RequestHandler`.

#### `def skipLinks(link)`

Method for checking if string contains a substring in the list `SKIP`. Reason for skipping these links can be found [here](#faq-sharer)

#### `def notShare(link)`

Method for checking if string contains a substring in the list `SHARER`. Reason for skipping these links can be found [here](#faq-skip)

#### `def scrapeSite(url)`

Method for crawling the website. It uses the python module `requests` to fetch the HTML content of the site. Then, the method parses the content using `BeautifulSoup` identifying elements with an `href` tag.

```python
		r = requests.get(url)
		html = r.content

		file = open("output.txt", 'a')
		file.write("Parsing: " + url + "\n")
		file.write("No. of OSAU links: " + str(len(osau_urls)) + "\n")
		file.write("No. of External links: " + str(len(ext_urls)) + "\n")
		file.close()

		soup = BeautifulSoup(html, 'html.parser')
		links = soup.find_all('a')
		urls = [link.get('href') for link in links if link.get('href') and (link.get('href')[0:4]=='http' or link.get('href')[0:5]=='https')]
```

After getting the links from the site, the script sorts the link if it is an internal link or an external links.

```python
		osau_temp = []
		ext_temp = []
		for link in urls:
			if link[0:21] == "http://localhost/osau" and skipLinks(link):
				osau_temp.append(link)

			elif skipLinks(link):
				if link not in list(ext_urls.keys()) and notShare(link):
					ext_urls[link] = url
```

To avoid duplicates, we check if the links we got is already in the list of links we have.

```python
		in_osau = set(osau_urls)
		in_temp = set(osau_temp)
		diff = in_temp - in_osau
		osau_urls = osau_urls + list(diff)
```

Then, we pass the new links in the method for crawling.

```python		
		for url in diff:
			scrapeSite(url)
```

Lastly, after crawling the site, we write the data we got in a file for future use.

```python
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
```

### `getheader.py`

`getheader.py` gets all links from `external.csv` generated from `deadlink.py` and stores it in a dictionary. The script only gets the header of the request instead of the whole content of the request (reasoning [here](#faq-why-header)). Depending on the HTTP code the link sends, the link is sorted whether it is working or not.

### `getall.py`

`getakk.py` gets all links from `links_with_error.csv` generated from `getheader.py` and stores it in a dictionary. The script gets the whole content of the link. Depending on the HTTP code the link sends, the link is sorted whether it is working or not.

### `getbrowser.py`

`getbrowser.py` gets all links from `links_with_error_2.csv` generated from `getall.py` and stores it in a dictionary. The script opens all links in the machine's default browser.

## FAQ


<div id="faq-sharer">
</div>

### 1. Why skip links with substrings in the list `SHARER`?

The `SHARER` variable is initialized as:

```python
SHARER = ['share.php', 'share?url', 'sharer.php']
```

These links are generated when sharing a school or an experience. Since this is dependent on social media sites, this will be blocked by the filter at the office. Also, there is no need to check these due to their purpose.

<div id="faq-skip">
</div>

### 2. Why skip links with substrings in the list `SKIP`?

The `SKIP` variable is initialized as:

```python
SKIP  = ['http://localhost/osau/questions', 'http://localhost/osau/search/school?loc=', 'http://localhost/osau/search/school?specialization=', 'http://localhost/osau/search/school?ranking=', 'http://localhost/osau/search/school?type=', 'http://localhost/osau/search/school?categ=']
```

These links are generated when viewing a question and searching for a school. Getting all of the links generated with these strings will take up a  __LOT__ of memory. Doing the math:

		There are 57 Locations, 2 Rankings, 5 School Type, 8 School Category and 258 School Specialization. 
		To find all possible links that can be generated:

			57*2**5*8*258 = 3,764,736 links

		But `school?loc=United+States&type=Private` is different from `school?type=Private&loc=United+States`, 
		so we need to multiply the number of possible ways to arrange the search terms which leads to:

			3764736*5! = 451,768,320 links

So it is imposibble to include all search term links when crawling the site.

<div id="faq-why-header">
</div>

### 3. Why get the header of a link first instead of getting the whole content of the link?

This is done mainly to save time. Getting the header uses less data than getting the whole HTML content. But a few sites responds with an error code when the request is header only. We use `getall.py` to double check if the links works or not. 

## Suggestions and Improvements

1. Use a desktop computer when running this script. Macbook sleeps when left unattended and stops all processes and needs to be plugged in at all times. Also, running multiple programs can slow down the script.

2. If you do use a Macbook, install Caffeine to prevent it from sleeping. Check the option `Prevent computer from sleeping automatically when the display is off`.

3. Some sites still responds with an error code when accessed using python requests probably protection from web crawling. I've already added more fields in the header of the request and lessen incorrect links that are working when accessed using a web browser.
