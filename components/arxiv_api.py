from xml.etree import ElementTree as ET

import requests, atoma

from . import arxiv_api, navigable_menus, feed

def endpoint():
    return "http://export.arxiv.org/api/query?"

def rss():
    return 'http://arxiv.org/rss/'

def get_feed(topic=None, STATE=None):
    if topic == None: raise Exception('you must provide an arxiv topic')
    if STATE == None: raise Exception('you must provide STATE')

    if getattr(STATE, topic) == []:
        r = requests.get(f"{arxiv_api.rss()}{topic}?version=2.0&mirror=in", timeout=10)
        root = ET.fromstring(r.content)
        feed_items = root.find('channel').findall('item')
        setattr(STATE, topic, feed_items)
    else:
        feed_items = getattr(STATE, topic)

    feed_items = [feed.Feed(f) for f in feed_items]
    return feed_items, STATE

def search(STATE=None):
    if STATE == None: raise Exception('You must provide STATE')

    if STATE.search_results == []:
        print('ti:title        au:author     abs:abstract      co:comment')
        print('jr:journal ref  cat:subj-cat  rn:report number')
        print(' ')
        query = input('Enter search term: ')
        if query == '':
            return [], STATE

        params = {
            'search_query': query,
            'start': 0,
            'max_results': 50,
            'sortBy': 'relevance',
            'sortOrder': 'descending'
        }
        query = '&'.join([str(x)+'='+str(y) for x, y in params.items()])

        r = requests.get(endpoint()+query, timeout=10)
        results = atoma.parse_atom_bytes(
            r.content
        ).entries
        STATE.search_results = results
    else:
        results = STATE.search_results

    results = [feed.Feed(r) for r in results]
    return results, STATE

def download(url):
    url = url.replace('/abs/', '/pdf/')
    r = requests.get(url, timeout=10)
    return r.content
