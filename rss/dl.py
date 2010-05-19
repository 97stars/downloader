import datetime
import logging
import os
import smtplib
import urllib2
from email.mime.text import MIMEText
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

def verify(db, config):
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    download_start = datetime.datetime.combine(yesterday, datetime.time(12))
    aired = [(":".join(e[:-1]).strip(), e[-1].strip()) for e in
             [x.split(":") for x in db.fetch_airdates(datetime.date.today())]]
    downloaded = db.fetch_releases(download_start,
                                   datetime.datetime.now())
    not_dl = []
    not_air = []
    for show, title in aired:
        fltr = _find_aired_filter(config.filters, show)
        match = False
        if fltr:
            for release in downloaded:
                match = match or fltr.match(release)
        if not match:
            not_dl.append((show, title))
            logger.warning("%s aired but didn't download", show)
    for release in downloaded:
        fltr = _find_release_filter(config.filters, release)
        match = False
        if fltr:
            for show, _ in aired:
                match = match or fltr.match(show)
            if not match:
                not_air.append(release)
                logger.warning("%s downloaded but didn't air", release)
    _mail(config.verify, aired, downloaded, not_dl, not_air)

def _find_release_filter(filters, string):
    for f in filters:
        if f.match(string):
            return f
    return None

def _find_aired_filter(filters, string):
    for f in filters:
        if f.match_include(string):
            return f
    return None

def _mail(config, aired, downloaded, not_dl, not_air):
    msg = MIMEText("The following aired but didn't download:\n" +
                   "\n".join([x[0] + ": " + x[1] for x in not_dl]) +
                   "\n\n" +
                   "The following downloaded but didn't air:\n" +
                   "\n".join(not_air) +
                   "\n\n" +
                   "The following aired:\n" +
                   "\n".join([x[0] + ": " + x[1] for x in aired]) +
                   "\n\n" +
                   "The following downloaded:\n" +
                   "\n".join(downloaded))
    msg["Subject"] = "Downloader report for %s" \
        % datetime.date.today().strftime("%a %b %d, %Y")
    msg["From"] = config.email
    msg["To"] = ", ".join(config.to)
    server = smtplib.SMTP("smtp.gmail.com:587")
    server.starttls()
    server.login(config.email, config.password)
    server.sendmail(config.email, config.to, msg.as_string())
    server.quit()

def _save(title, url, directory):
    title = re.sub(r'\/:*?"<>|', "_", title)
    t_url = urllib2.urlopen(url)
    with TemporaryFile() as temp:
        temp.write(t_url.read())
        temp.seek(0, os.SEEK_SET)
        with open(os.path.join(directory, title + ".torrent"), "wb") as out:
            out.write(temp.read())
