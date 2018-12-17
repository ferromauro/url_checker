#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 15 17:13:33 2018

@author: Mauro Ferro
Poject Name: Link Checker
Filename: linkCheker.py

"""
from lxml import html
from urllib.parse import urlparse
import requests, sys, getopt, os, validators

# define global variables
urls=[]
url_checked=[]
url_to_check=[]
bad_links=[]
not_checked=[]
url_to_scrape=''
domain = ''
limit=None
i=0
# start the job
def main(argv):
    initialize(argv)
    while len(url_to_check)>0:
        url=url_to_check[0]
        looper(url)
    print_result()
    
    
def get_links(url):
    page = requests.get(url)
    if page.status_code == 404:
        bad_links.append(url)
        return
    else:
        webpage = html.fromstring(page.content)
        urls = webpage.xpath('//a/@href')
        for url in urls:
            o = urlparse(url)
            if o.netloc == domain:
                check_duplicate(url)   # verifica se già in lista o già verificati
            
def initialize(argv):
    global domain
    global limit
    global url_to_check
    try:
      opts, args = getopt.getopt(argv,"hu:l:",["help","url","limit"])
    except getopt.GetoptError:
      logo()  
      print('Usage: linkChecker.py -u <url_website> [-l <url_limit>]')
      sys.exit(2)
    if opts==[]:
      logo()  
      print('Usage: linkChecker.py -u <url_website> [-l <url_limit>]')
      sys.exit(2)  
    for opt, arg in opts:
        if opt in ('-h', "--help"):
            logo()
            print('Usage: linkChecker.py -u <url_website> [-l <url_limit>]')
            sys.exit()
        elif opt in ("-l","--limit"):
            limit=arg
        elif opt in ("-u", "--url"):
            if validators.url(arg):
                url_to_scrape = arg     
                url_to_check.append(url_to_scrape)
                domain=urlparse(url_to_scrape).netloc

            else:
                logo()
                print('Please insert a valid url.')
                sys.exit()
    
def check_duplicate(url):
    global url_to_check
    global url_checked
    if url in url_to_check:
        return
    if url in url_checked:
        return
    else:
        url_to_check.append(url)
        return url_to_check
        
def update_lists(url):
    global url_to_check
    global url_checked
    url_to_check = [x for x in url_to_check if x != url] 
    url_checked.append(url)           
    return

def looper(url):
    global i
    global url_to_check
    if limit == None or i<limit:
        try: 
            print(f'Scanning: {url}')
            get_links(url)   # estrai i link dalla pagina 
        except:
            not_checked.append(url)
        update_lists(url)       # aggiorna le liste      
        os.system('clear')
        logo()
        print(f'Checked: {len(url_checked)} links.')
        print(f'Links to check: {len(url_to_check)}')
        print(f'Founded {len(bad_links)} 404 error pages!')
        i=i+1
        return
    url_to_check=[]    
    
  
def print_result():
    with open('url_checked.txt', 'w') as f:
        for line in url_checked:
            f.write(f'{line}\n') 
    print(f'Total pages scanned: {len(url_checked)}')
    print(f'Scan completed, founded {len(bad_links)} page 404' )
    if len(bad_links)>0:
        with open('bad_urls.txt', 'w') as f:
            for line in bad_links:
                f.write(f'{line}\n')
        print(f'{bad_links}')
    print('END')
        
def logo():
    print('*'*20)
    print('*'*40)
    print('*'*60)
    print('*'*20+' URL CHECKER '+'*'*37)
    print('*'*60)
    print('*'*40)
    print('*'*20)

if __name__ == "__main__":
    main(sys.argv[1:])
    