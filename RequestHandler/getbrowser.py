# System modules
import webbrowser
import csv

# Get all links with error generated by getall.py from a csv file
with open('links_with_error_2.csv', 'r') as f:
    reader = csv.reader(f)
    links = list(reader)

# Open them in a browser
for link in links:
	webbrowser.open(link[0])