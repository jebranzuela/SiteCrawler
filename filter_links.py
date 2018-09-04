import csv
import sys
from collections import defaultdict

HEADERS = ["link", "source"]

def read_csv(csv_file):
	data = defaultdict(list)
	reader = csv.DictReader(csv_file, fieldnames=HEADERS)
	next(reader)

	for row in reader:
		key = row.pop("link")

		if key not in list(data.keys()):
			data[key].append(row)

	return data

with open('external.csv') as source:
	links = read_csv(source)

print links