#!/usr/bin/python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from json import loads
from urllib.request import urlopen
from urllib.parse import urlencode, unquote
import ssl

def getJSON(page):
    params = urlencode({
      'format': 'json',
      'action': 'parse',
      'prop': 'text',
      'redirects': 'true',
      'page': page})
    API = "https://en.wikipedia.org/w/api.php"
    # we generate a SSL certificate
    gcontext = ssl.SSLContext()
    response = urlopen(API + "?" + params, context=gcontext)
    return response.read().decode('utf-8')


def getRawPage(page):
    parsed = loads(getJSON(page))
    try:
        title = parsed['parse']['title']
        content = parsed['parse']['text']['*']
        return title, content
    except KeyError:
        # the requested page dosn't exist
        return None, None


def getPage(page):
    title, content = getRawPage(page)

    if (title, content) == (None, None):
        # the requested page dosn't exist
        return None, []
    soup = BeautifulSoup(content, features='html.parser')

    links = []
    limit = 10
    n = 0
    # we select only the p elements which are directly a child of the div element at the root of the HTML page
    for p in soup.find('div', recursive=True).find_all('p', recursive=False):
        # only the first 10 items are returned
        if n >= limit:
            break
        for a in p.find_all('a', href=True):
            if n >= limit:
                break
            # we filter the red links (attribut class = 'new')
            # and external links
            if not (a.has_attr('class') and 'new' in a['class']) \
                and not a['href'].startswith('http') \
                and not a['href'].startswith('//'): #and not a['href'].startswith('#'):
                link = unquote(a['href'].split("/wiki/")[-1]).split("#")[0].replace('_', ' ')
                # we want to avoid duplicates and empty links
                if (link not in links) and link != '' and ':' not in link:
                    links.append(link)
                    n += 1

    return title, links

if __name__ == '__main__':
    # can be used for test purposes
    # print(getPage(Test"))
    pass

