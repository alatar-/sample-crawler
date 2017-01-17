import datetime

from .helpers import get_url_soup, translate_timestamp


def crawl_catalog_pages(url, timestamp):
    '''Crawl one page of the catalog and store entries. '''
    soup = get_url_soup(url)
    listings = soup.find_all('article', 'offer-item')
    for l in listings:
        offer = parse_catalog_listing(l)

        # if general listing doesn't provide dealer information
        # crawl its detail page
        if 'dealer' not in offer:
            soup = get_url_soup(offer['url'])
            offer = parse_offer_page(soup, offer)

        # TODO: save to db

        if not offer['promoted'] and \
           offer.get('timestamp', datetime.datetime.now()) < timestamp:
                break

    next_page_url = get_next_page_url(soup)
    if next_page_url:
        crawl_catalog_pages(next_page_url, timestamp)


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
