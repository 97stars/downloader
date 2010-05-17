from optparse import OptionParser, make_option

from rss.config import Config
from rss.db import RecordDB
from rss.parsers import EZRSS

OPTIONS = [
    make_option("-c", "--config", action="store",
                type="string", dest="config", metavar="FILE"),
    make_option("-v", "--verify", action="store_true",
                dest="verify", default=False),
    make_option("-a", "--airdate", action="store_true",
                dest="airdate", default=False)]


def parse_options():
    parser = OptionParser(option_list=OPTIONS)
    (options, args) = parser.parse_args()
    if not options.config:
        parser.error("config option is manditory")
    return (options, args)


def main():
    (options, args) = parse_options()
    config = Config(options.config)
    if options.verify:
        print "VERIFY"
    elif options.airdate:
        print "AIRDATE"
    else:
        releases = EZRSS(config.url).parse()
        for r, _ in releases:
            print r


if __name__ == '__main__':
    main()
