"""
  Download mp3 Bible sermons by Chuck Smith. Requires Beautiful Soup
"""

import urllib2
from os import popen

from bs4 import BeautifulSoup

page = urllib2.urlopen("http://twft.com/?page=c2000")
page_html = page.read()
page.close()

soup = BeautifulSoup(page_html, 'html5lib')
all_href = soup.findAll('a')

location_to_save = '/home/britone/Music/bible'

mp3_links = []

for href in all_href:
    if 'mp3' in str(href.get('href')):
         mp3_links.append(href.get('href'))

for link in mp3_links:
    args = ['wget %s', '-r', '-l 1', '-p', '-P %s' % location_to_save, link]
    output = popen(' '.join(args))
    print output
