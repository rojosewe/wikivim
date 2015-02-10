import sys
from bs4 import BeautifulSoup
import urllib2


arguments = sys.argv[1:]
#arguments = ["kindle"]
entity = "_".join(arguments)
separator = """
"""
url = 'http://en.wikipedia.org/wiki/' + entity + '_(disambiguation)'
page = urllib2.urlopen(url).read()
soup = BeautifulSoup(page)
tags = soup.find(id='mw-content-text').find_all('a')
for link in soup.find_all('a'):
    foundValue = False
    title = link.get('title')
    if(title is not None):
        for arg in arguments:
            foundValue = foundValue or any(arg.lower() in s.lower() for s in title.split(" "))
        if(foundValue):
            print("wiki " + title.replace("(", "\(").replace(")", "\)"))