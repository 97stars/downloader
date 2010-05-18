import datetime
import time
import logging
import sqlite3

logger = logging.getLogger("downloader.rss")


class RecordDB(object):

    def __init__(self, filename):
        self.conn = sqlite3.connect(filename)
        self.__create()

    def add(self, release):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO downloaded(title, time) VALUES(?, ?);",
                    (release, time.time()))
        self.conn.commit()
        cur.close()

    def add_airdate(self, show):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO airdates(show, time) VALUES(?, ?);",
                    (show, time.time()))
        self.conn.commit()
        cur.close()

    def exists(self, release):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM downloaded WHERE title = ?;", (release,))
        cur.close()
        if cur.fetchone() != None:
            return True
        else:
            return False

    def fetch_airdates(date):
        cur = self.conn.cursor()
        cur.execute("SELECT show, time FROM airdates;")
        return [row[0] for row in cur.fetchall()
                if datetime.datetime.fromtimestamp(float(row[1])).date() ==
                date]

    def fetch_releases(timestart, timeend):
        cur = self.conn.cursor()
        cur.execute("SELECT title, time FROM downloaded;")
        return [row[0] for row in cur.fetchall()
                if (datetime.datetime.fromtimestamp(float(row[1])) >= timestart
                    and
                    datetime.datetime.fromtimestamp(float(row[1])) <= timeend)]

    def __create(self):
        cur = self.conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS downloaded
(id INTEGER PRIMARY KEY, title VARCHAR(255), time VARCHAR(32));""")
        cur.execute("""CREATE TABLE IF NOT EXISTS airdates
(id INTEGER PRIMARY KEY, show VARCHAR(255), time VARCHAR(32));""")
        self.conn.commit()
        cur.close()
