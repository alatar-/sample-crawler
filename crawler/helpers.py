import datetime

import requests
from bs4 import BeautifulSoup


def translate_timestamp(ts):
    translation = {
        'stycznia': 1,
        'lutego': 2,
        'grudnia': 12
    }

    def multiple_replace(text, _dict):
        for key in _dict:
            text = text.replace(key, str(_dict[key]))
        return text

    ts = multiple_replace(ts, translation)
    ts = datetime.datetime.strptime(ts, '%H:%M, %d %m %Y')

    return ts


def get_url_soup(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.content, 'html.parser')

    return soup
