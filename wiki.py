import newspaper
import sys
import subprocess
from bs4 import BeautifulSoup
import urllib2

arguments = sys.argv[1:]
separator = """
    """
#arguments = ["kindle"]

def wikiDisambiguation(linker, titleList):
    url = 'http://en.wikipedia.org' + str(linker)
    page = urllib2.urlopen(url).read()
    soup = BeautifulSoup(page)
    tags = soup.find(id='mw-content-text').find_all('a')
    for link in soup.find_all('a'):
        foundValue = False
        title = link.get('title')
        if(title is not None):
            for arg in titleList.split(" "):
                foundValue = foundValue or any(arg.lower() in s.lower() for s in title.split(" "))
            if(foundValue):
                print("wiki " + title.replace("(", "\(").replace(")", "\)"))

def wikiSug():
    entity = "+".join(arguments)
    url = 'https://en.wikipedia.org/w/index.php?title=Special%3ASearch&profile=default&search='+entity+'&fulltext=Search'
    page = urllib2.urlopen(url).read()
    soup = BeautifulSoup(page)
    tags = soup.find_all(class_='mw-search-result-heading')
    for link in tags:
        foundValue = False
        title = link.find('a').get('title')
        if(title is not None):
            if("(disambiguation)" in title):
                wikiDisambiguation(link.find('a').get('href'), title.replace(" (disambiguation)", ""))
            else:
                for arg in arguments:
                    foundValue = foundValue or any(arg.lower() in s.lower() for s in title.split(" "))
                if(foundValue):
                    print("wiki " + title.replace("(", "\(").replace(")", "\)"))

def wikiSearch():
    entity = "_".join(arguments)
    url = 'http://en.wikipedia.org/wiki/'+entity
    #url = 'http://en.wikipedia.org/w/api.php?action=query&prop=revisions&redirects=&titles='+entity+'&rvprop=content&format=json'
    article = newspaper.Article(url, language='en')
    article.download()
    article.parse()
    article.nlp()
    
    printList = []
    printList.append("*URL:* " + url)
    printList.append(separator)
    printList.append("*Title:* "+" ".join(arguments)) 
    printList.append("*Keywords:* " + str(article.keywords))
    printList.append(separator)
    printList.append("*Summary*")
    printList.append(article.text.encode('UTF-8').split("\n")[0])
    printList.append(article.summary.encode('UTF-8'))
    printList.append(separator)
    printList.append("*Wikipedia text*")
    printList.append(article.text.encode('UTF-8'))
    printList.append(separator)
    printList.append("*Images*")
    printList.append(str(article.images))
    printList.append(separator)
    #print("\n".join(printList))
    #print(" ".join(["echo", "\n".join(printList), "|", "vim", "-","+/*.*"]))
    
    p1 = subprocess.Popen(["echo", "\n".join(printList)], stdout=subprocess.PIPE)
    p2 = subprocess.Popen(["vim", "-","+/*.*"], stdin=p1.stdout)
    p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
    output,err = p2.communicate()

if(any("-s" == s.lower() for s in arguments)):
    arguments.remove("-s")
    wikiSug()
else:
    wikiSearch()