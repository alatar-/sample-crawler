import datetime
import logging

import crawler.config as cfg
from .parsers import crawl_catalog_pages, crawl_dealers_pages, crawl_phone_number
from .db import PseudoDB
from .helpers import send_sms

OTOMOTO_DEALERS_CATALOG_URL = 'https://www.otomoto.pl/osobowe/%(city)s/?search%%5Bfilter_enum_authorized_dealer%%5D=1&search%%5Bdist%%5D=%(distance)d&search%%5Bcountry%%5D='
OTOMOTO_PHONE_NUMBER_URL = 'https://www.otomoto.pl/ajax/misc/contact/multi_phone/%s/1'

logger = logging.getLogger(__name__)


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

    logger.info("Crawling catalog pages starting from the base url.")
    crawl_catalog_pages(url, timestamp)


def crawl_changes():
    '''Crawl otomoto.pl dealers pages and detect which offers has finished.'''
    logger.info("Crawling current offers ids.")
    offers_current = crawl_dealers_pages()

    with PseudoDB() as db:
        logger.info("Comparing current offers to previously scraped db.")
        offers_finished = set()
        for offer_id in db.get_offers_gen():
            if offer_id not in offers_current:
                offers_finished.add(offer_id)

        logger.info("Processing finished offers.")
        for offer_id in offers_finished:
            logger.debug("Removing stored offer %s." % offer_id)
            offer = db.drop_offer(offer_id)

            number = crawl_phone_number(OTOMOTO_PHONE_NUMBER_URL, offer['url'])
            if number:
                send_sms(number)
