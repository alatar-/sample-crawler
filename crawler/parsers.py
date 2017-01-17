import datetime
import logging

import crawler.db as db
from .helpers import get_url_soup, translate_timestamp


logger = logging.getLogger(__name__)


def crawl_catalog_pages(url, timestamp, db_handle):
    '''Crawl one page of the catalog and store entries. '''
    logger.info("Crawling catalog page (%s)" % url)
    soup_catalog = get_url_soup(url)
    listings = soup_catalog.find_all('article', 'offer-item')
    for l in listings:
        offer = parse_catalog_listing(l)
        logger.info("Parsed offer listing (%s)." % offer['id'])

        if 'dealer' not in offer:
            logger.info("Dealer info not found. Crawling details page.")
            soup_offer = get_url_soup(offer['url'])
            offer = parse_offer_page(soup_offer, offer)

        db.store_offer(offer, db_handle)

        if not offer['promoted'] and \
           offer.get('timestamp', datetime.datetime.now()) < timestamp:
                break

    next_page_url = get_next_page_url(soup_catalog)
    if next_page_url:
        crawl_catalog_pages(next_page_url, timestamp, db_handle)


def parse_offer_page(soup, offer):
    '''Parse offer details page for timestamp and dealer info.'''
    timestamp = soup.find('span', 'offer-meta__item').find('span', 'offer-meta__value').get_text()

    offer['timestamp'] = translate_timestamp(timestamp)
    offer['dealer'] = soup.find('h2', 'seller-box__seller-name').a['href']
    return offer


def parse_catalog_listing(l):
    offer = {}
    offer['promoted'] = 'promoted' in l['class']

    l_a = l.find('h2', 'offer-title').a
    offer['title'] = l_a.get_text().strip()
    offer['id'] = l_a['data-ad-id']
    offer['url'] = l_a['href']

    l_d = l.find('div', 'seller-logo')
    if l_d is not None:
        offer['dealer'] = l_d.a['href']
    
    return offer


def get_next_page_url(soup):
    next_page = soup.find('ul', 'om-pager').find('li', 'next')
    if next_page:
        return next_page.a['href']
    else:
        return None
