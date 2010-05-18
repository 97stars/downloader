import logging
import os
import urllib2
from tempfile import TemporaryFile

logger = logging.getLogger("downloader.rss.dl")

def fetch(releases, directory, db):
    for title, url in releases:
        if db.exists(title):
            logger.info("%s has already been downloaded", title)
        else:
            _save(title, url, directory)
            db.add(title)
            logger.info("%s downloaded", title)

def record_airdates(airdates, db):
    for a in airdates:
        db.add_airdate(a)
        logger.info("Airdate %s added", a)

def verify():
    pass

def _save(title, url, directory):
    t_url = urllib2.urlopen(url)
    with TemporaryFile() as temp:
        temp.write(t_url.read())
        temp.seek(0, os.SEEK_SET)
        with open(os.path.join(directory, title + ".torrent"), "wb") as out:
            out.write(temp.read())
