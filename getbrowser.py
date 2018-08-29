import webbrowser

with open('links_with_error_2.txt', 'r') as f:
    links = [line.strip() for line in f]

for url in urls:
	webbrowser.open(url)