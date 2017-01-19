#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Twitter AcronyBot
# This script scraps the list of acronyms from
# http://www.netlingo.com/acronyms.php
# shuffle them and store them in a file


import requests
from bs4 import BeautifulSoup
import sys
import urllib2
import time
import os

COUNTRIES = "countries"
SECTORS = "sectors"


if not os.path.exists(COUNTRIES):
        os.makedirs(COUNTRIES)
if not os.path.exists(SECTORS):
        os.makedirs(SECTORS)


def download_file(type, download_url, name):
    response = urllib2.urlopen(download_url)
    if type == "countries":
        file = open(COUNTRIES+"/"+name+".pdf", 'w')
    else:
        file = open(SECTORS+"/"+name+".pdf", 'w')
    print "nombre:",name
    file.write(response.read())
    file.close()
    print("Completed")


def scrape(result, type):
    if result.status_code != 200:
        sys.exit("Error accessing the url. Scraping aborted!!")
    else:
        soup = BeautifulSoup(result.content, "html.parser")
        table = soup.find("div"," colSize0 col-xs-12 div-content col-md-0 outpadding richText")
        for i,line in enumerate(table.find_all("li")):
            link = line.a["href"] 
            if link.startswith("/"):
                link = "http://www.iadb.org" + link 

            name = line.a.string
            print link
            # substitute all kind of whitespaces for normal whitespaces
            name_adjusted = " ".join(name.split())
            name_score = name_adjusted.replace(" ", "_").replace(":","")
            print name_score
            download_file(type, link, name_score)
            # wait 1 second between downloads
            time.sleep(1)


result = requests.get("http://www.iadb.org/en/about-us/country-strategies,7809.html")
scrape(result,"countries")
result = requests.get("http://www.iadb.org/en/about-us/sector-strategies,1326.html")
scrape(result,"sectors")


# download_file("http://www.iadb.org/document.cfm?id=36174731")
