import logging
import logging.handlers
from optparse import OptionParser, make_option

from rss import dl
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


def main(config, options):
    if options.verify:
        print "VERIFY"
    elif options.airdate:
        print "AIRDATE"
    else:
        releases = EZRSS(config.url).parse()
        dl.fetch([(title, url) for title, url in releases if
                  reduce(lambda x, y: x or y,
                         [f.match(title) for f in config.filters])],
                 config.output_folder)


def get_logger(filename):
    my_logger = logging.getLogger("downloader")
    formatter = logging.Formatter(
        "%(asctime)s %(name)-20s %(levelname)-8s %(message)s",
        "%m-%d %H:%M")
    filelogger = logging.handlers.TimedRotatingFileHandler(
        filename,
        "D",
        7,  # seven days of logs in one file
        8)  # 8 weeks worth of logs
    filelogger.setLevel(logging.DEBUG)
    filelogger.setFormatter(formatter)
    my_logger.addHandler(filelogger)
    my_logger.setLevel(logging.DEBUG)
    return my_logger

if __name__ == '__main__':
    (options, args) = parse_options()
    config = Config(options.config)
    logger = get_logger(config.logfile)
    try:
        main(config, options)
        logger.info("DONE")
    except Exception as e:
        logger.error(e)
