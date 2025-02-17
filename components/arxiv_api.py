"""
ArXiv CLI Browser - a command line interface browser for the popular pre-print
academic paper website https://arxiv.org

Copyright (C) 2020  Klinkesorn Nguyen An Hoa

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

Author contactable at k<dot>nguyen<dot>an<dot>hoa<at>gmail<dot>com
"""

from xml.etree import ElementTree as ET

import requests, atoma

from . import arxiv_api, navigable_menus, feed

def endpoint():
    return "http://export.arxiv.org/api/query?"

def rss():
    return 'http://rss.arxiv.org/rss/'

def get_feed(topic=None, STATE=None):
    print(' ')
    print('STANDBY...')
    if topic == None: raise Exception('you must provide an arxiv topic')
    if STATE == None: raise Exception('you must provide STATE')

    if getattr(STATE, topic) == []:
        r = requests.get(f"{arxiv_api.rss()}{topic}", timeout=10)
        root = ET.fromstring(r.content)
        feed_items = root.find('channel').findall('item')
        setattr(STATE, topic, feed_items)
    else:
        feed_items = getattr(STATE, topic)

    feed_items = [feed.Feed(f) for f in feed_items]
    if feed_items == []: navigable_menus.error('No feed found (server could be down, or it is Sat/Sun)')
    return feed_items, STATE

def parse_search_query(query):
    query = query.replace(' ', '+')
    query = query.replace('(', '%28')
    query = query.replace(')', '%29')

    return query

def search(STATE=None):
    if STATE == None: raise Exception('You must provide STATE')

    if STATE.search_results == []:
        query = input('Enter search term: ')
        if query == '':
            return [], STATE

        query = parse_search_query(query)
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
