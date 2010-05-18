import os
import urllib2
from tempfile import TemporaryFile

from rss.db import RecordDB


def fetch(releases, directory):
    for title, url in releases:
        _save(title, url, directory)


def record_airdates(airdates):
    pass

def verify():
    pass


def _save(title, url, directory):
    t_url = urllib2.urlopen(url)
    with TemporaryFile() as temp:
        temp.write(t_url.read())
        temp.seek(0, os.SEEK_SET)
        with open(os.path.join(directory, title + ".torrent"), "wb") as out:
            out.write(temp.read())
