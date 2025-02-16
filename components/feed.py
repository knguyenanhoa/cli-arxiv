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

import re, copy, sys, os, time

from pdfminer.high_level import extract_text

from components import navigable_menus, arxiv_api

class Feed():
    def __new__(cls, feed):
        if feed.__class__.__name__ == 'AtomEntry':
            return AtomFeed(feed)
        else:
            return XMLFeed(feed)

    def title(self):
        raise Exception('abstract class')

    def summary(self):
        raise Exception('abstract class')

    def published(self):
        raise Exception('abstract class')

    def clean(self, feed):
        raise Exception('abstract class')

    def view(self):
        return self.clean(self.summary())

    def download(self):
        print('-'*80)
        link = self.pdf_link()

        if os.path.exists(f"./data/summary/{self.title()}.txt"):
            print('summary file already exists')
        else:
            print('saving summary...')
            with open(f"./data/summary/{self.title()}.txt", 'w') as f:
                f.write(self.summary())

        if os.path.exists(f"./data/pdf/{self.title()}.pdf"):
            print('pdf file already exists. download halted.')
        else:
            print('downloading pdf...')
            pdf = arxiv_api.download(link)
            with open(f"./data/pdf/{self.title()}.pdf", 'wb') as f:
                f.write(pdf)
            with open(f"./data/to-read/{self.title()}.pdf", 'wb') as f:
                f.write(pdf)

        if os.path.exists(f"./data/txt/{self.title()}.txt"):
            print('text file already exists. conversion halted.')
        else:
            print('converting pdf to txt..')
            with open(f"./data/txt/{self.title()}.txt", 'w') as f:
                f.write(self.text())

        print('done')
        time.sleep(0.5)

    def text(self):
        return extract_text(f"./data/pdf/{self.title()}.pdf")




class XMLFeed(Feed):
    def __new__(cls, feed):
        return object.__new__(cls)

    def __init__(self, feed):
        self.feed = feed

    def title(self):
        title = self.feed.find('title').text
        title = re.sub("[\.\:\[\]]", "", title)
        return f"{title} (Preprint)"

    def summary(self):
        return self.feed.find('description').text.lower()

    def clean(self, feed):
        feed = feed.replace("<p>","").replace("</p>","")
        feed = re.sub("<a href=\"[\S][^,]*\">", '', feed)
        feed = feed.replace("</a>", "")
        return feed

    def pdf_link(self):
        return self.feed.find('link').text





class AtomFeed(Feed):
    def __new__(cls, feed):
        return object.__new__(cls)

    def __init__(self, feed):
        self.feed = feed

    def summary(self):
        return f"{self.short_authors()}\n\n{self.feed.summary.value}\n".lower()

    def published(self):
        return self.feed.published.strftime('%Y')

    def authors(self):
        return ', '.join([author.name for author in self.feed.authors])

    def short_authors(self):
        if len(self.feed.authors) < 3:
            return self.authors()
        else:
            return f"{self.feed.authors[0].name} et al"

    def title(self):
        title = self.feed.title.value
        title = re.sub("[\.\:\[\]]", "", title)
        return f"{title} ({self.short_authors()} {self.published()})"

    def clean(self, feed):
        return feed

    def pdf_link(self):
        return self.feed.id_
