import os
import re
import yaml


class FilterData(object):

    def __init__(self, data):
        self._include = re.compile(data["include"], re.IGNORECASE)
        self._exclude = re.compile(data["exclude"], re.IGNORECASE)
        self._name = data["name"]

    @property
    def name(self):
        return self._name

    def match(self, string):
        return (self._include.search(string) and not
                self._exclude.search(string))

    def match_include(self, string):
        return self._include.search(string)


class Verify(object):

    def __init__(self, data):
        self._url = data["url"]
        self._email = data["email"]
        self._password = data["password"]
        self._to = data["to"]

    @property
    def email(self):
        return self._email

    @property
    def password(self):
        return self._password

    @property
    def to(self):
        return self._to

    @property
    def url(self):
        return self._url


class Config(object):

    def __init__(self, filename):
        self._database = None
        self._logfile = None
        self._filters = []
        self._outdir = None
        self._url = None
        self._verify = None
        with open(filename) as f:
            self.__load(yaml.load(f))

    @property
    def database(self):
        return self._database

    @property
    def logfile(self):
        return self._logfile

    @property
    def filters(self):
        return self._filters

    @property
    def output_folder(self):
        return self._outdir

    @property
    def url(self):
        return self._url

    @property
    def verify(self):
        return self._verify

    def __load(self, data):
        for entry in data:
            if entry == "database":
                self._database = data[entry]
            elif entry == "output_directory":
                self._outdir = data[entry]
            elif entry == "logfile":
                self._logfile = data[entry]
            elif entry == "url":
                self._url = data[entry]
            elif entry == "filters":
                for f in data[entry]:
                    self._filters.append(FilterData(f))
            elif entry == "verify":
                self._verify = Verify(data[entry])
            else:
                print "Unreconized config option %s" % entry
                sys.exit(1)
