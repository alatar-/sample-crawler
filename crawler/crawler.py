import datetime
import requests
from bs4 import BeautifulSoup

import crawler.config as cfg
from .parsers import parse_offer

OTOMOTO_DEALERS_CATALOG_URL = 'https://www.otomoto.pl/osobowe/%(city)s/?search%5Bfilter_enum_authorized_dealer%5D=1&search%5Bdist%5D=%(distance)d&search%5Bcountry%5D='


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


def crawl_catalog_pages(url, timestamp):
    '''Crawl one page of the catalog and store entries. '''
    soup = get_url_soup(url)
    listings = soup.find_all('article', 'offer-item')
    for l in listings:
        offer = parse_offer(l)

        # if general listing doesn't provide dealer information
        # crawl its detail page
        if 'dealer' not in offer:
            offer = crawl_offer_page(offer)

        # TODO: save to db

        if not offer['promoted'] and \
           offer.get('timestamp', datetime.datetime.now()) < timestamp:
                break

    next_page = soup.find('ul', 'om-pager').find('li', 'next')
    if next_page:
        next_page_url = next_page.a['href']
        crawl_catalog_pages(next_page_url, timestamp)


def crawl_offer_page(offer):
    '''Crawl offer details page for timestamp and dealer info.'''
    soup = get_url_soup(offer['url'])
    offer['timestamp'] = soup.find('span', 'offer-meta__item').find('span', 'offer-meta__value').get_text()
    offer['dealer'] = soup.find('h2', 'seller-box__seller-name').a['href']
    return offer


def get_url_soup(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.content, 'html.parser')

    return soup
