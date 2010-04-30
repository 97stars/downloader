import feedparser
import logging

logger = logging.getLogger("downloader.rss")


class EZRSS(object):

    def __init__(self, url):
        self.url = url

    def parse(self):
        feed = feedparser.parse(self.url)
        return ((r.title, r.link) for r in feed.entries)


class TVDB(object):

    def __init__(self, url):
        self.url = url

    def parse(self):
        feed = feedparser.parse(self.url)
        return (e.title.strip() for e in feed.entries)
