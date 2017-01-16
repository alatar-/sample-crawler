import requests
from bs4 import BeautifulSoup

import crawler.config as cfg
from .parsers import parse_offer

OTOMOTO_URL = 'https://www.otomoto.pl/osobowe/%(city)s/?search%%5Bdist%%5D=%(distance)d&search%%5Bcountry%%5D=&page=%(page)d'


def crawl_offers_catalog(page=1):
    result = requests.get(OTOMOTO_URL % {**cfg.otomoto, 'page': page})
    soup = BeautifulSoup(result.content, 'html.parser')
    listings = soup.find_all('article', 'offer-item')
    for l in listings:
        print(parse_offer(l))
        break
