import webbrowser
import csv

# with open('links_with_error_2.txt', 'r') as f:
#     links = [line.strip() for line in f]

with open('links_with_error_2.csv', 'r') as f:
    reader = csv.reader(f)
    links = list(reader)

for link in links:
	webbrowser.open(link[0])