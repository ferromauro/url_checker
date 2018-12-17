# url_checker
Crawler to inspect presence of 404 error pages in websites. 

This simple program scans a website for corrupt links that point to a non-existent page and then to a '404 page not found' server response.
At the end of the scan a file will be produced (url_checkes.txt) with the list of all scanned url addresses.
If errors are found they will be written to another page (bad_urls.txt).

# Usage 

python3 url_checker -u <website_url> [-l <limit_url>]

example: python3 url_checker.py -u 'www.github.com' -l 100
