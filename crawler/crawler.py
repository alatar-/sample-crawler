import datetime

import crawler.config as cfg
from .parsers import crawl_catalog_pages

OTOMOTO_DEALERS_CATALOG_URL = 'https://www.otomoto.pl/osobowe/%(city)s/?search%%5Bfilter_enum_authorized_dealer%%5D=1&search%%5Bdist%%5D=%(distance)d&search%%5Bcountry%%5D='


def crawl_catalog(timestamp=None):
    '''Crawl otomoto.pl catalog and save the offers from dealers
    incrementaly, based on the last timestamp.

    NOTE: Timestamp testing is irregular so it may crawl many
    redundant offers before terminated.

    :param timestamp: A datetime of last crawling execution.
    '''
    url = OTOMOTO_DEALERS_CATALOG_URL % cfg.otomoto
    if not timestamp:
        timestamp = datetime.datetime(2000, 1, 1)

    crawl_catalog_pages(url, timestamp)
