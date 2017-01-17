import logging
import datetime

import requests
from bs4 import BeautifulSoup
from twilio.rest import TwilioRestClient

from .config import twilio

logger = logging.getLogger(__name__)


def translate_timestamp(ts):
    translation = {
        'stycznia': 1,
        'lutego': 2,
        'grudnia': 12,
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


def send_sms(number):
    assert len(number) == 9

    client = TwilioRestClient(twilio['sid'], twilio['token'])
    message = client.messages.create(to="+48%s" % number, from_=twilio['origin-number'],
                                     body=twilio['message'])
    return message
