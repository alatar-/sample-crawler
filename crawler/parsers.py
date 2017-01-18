import datetime
import logging
from json import JSONDecodeError

from .helpers import get_url_soup, translate_timestamp, get_url_json
from .db import PseudoDB

logger = logging.getLogger(__name__)


def crawl_catalog_pages(url, timestamp):
    '''Iteratively crawl catalog pages and store offer entries.'''
    with PseudoDB() as db:
        while True:
            logger.info("Crawling catalog page (%s)" % url)
            soup_catalog = get_url_soup(url)

            listings = soup_catalog.find_all('article', 'offer-item')
            for l in listings:
                offer = parse_catalog_listing(l)
                logger.debug("Parsed offer listing (%s)." % offer['id'])

                if 'dealer' not in offer:
                    logger.debug("Dealer info not found. Crawling details page.")
                    soup_offer = get_url_soup(offer['url'])
                    offer = parse_offer_page(soup_offer, offer)

                db.store_offer(offer)

                if not offer['promoted'] and \
                   offer.get('timestamp', datetime.datetime.now()) < timestamp:
                        break

            url = get_next_page_url(soup_catalog)
            if not url:
                break


def crawl_dealers_pages():
    '''Crawl dealers pages and return current offers ids..'''
    dealers = None
    with PseudoDB() as db:
        dealers = db.get_dealers()

    current_offers = set()
    # import pdb; pdb.set_trace()
    for url in dealers:
        while True:
            logger.info("Crawling dealers page (%s)" % url)
            soup_catalog = get_url_soup(url)
            listings = soup_catalog.find_all('article', 'offer-item')
            for l in listings:
                offer = parse_catalog_listing(l)
                logger.debug("Parsed offer listing (%s)." % offer['id'])
                current_offers.add(offer['id'])

            url = get_next_page_url(soup_catalog)
            if not url:
                break

    return current_offers


def crawl_phone_number(req_url, offer_url):
    req_id = offer_url[:offer_url.find('.html')][-6:]
    logger.debug("Crawling phone number for request id %s." % req_id)
    try:
        _json = get_url_json(req_url % req_id)
    except JSONDecodeError:
        logger.warning("Phone number for the dealer can't be retrieved.")
        return None

    number = _json.get('value')
    return number


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
    if l_d is not None and l_d.a:
        offer['dealer'] = l_d.a['href']
    
    return offer


def get_next_page_url(soup):
    next_page = soup.find('li', 'next')
    if next_page:
        return next_page.a['href']
    else:
        return None
