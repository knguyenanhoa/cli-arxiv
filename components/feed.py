import re, copy, sys, os, time
from components import navigable_menus, arxiv_api
from pdfminer.high_level import extract_text

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
        return title

    def summary(self):
        return self.feed.find('description').text

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
        return self.feed.summary.value

    def title(self):
        title = self.feed.title.value
        title = re.sub("[\.\:\[\]]", "", title)
        return title

    def clean(self, feed):
        return feed

    def pdf_link(self):
        return self.feed.id_
