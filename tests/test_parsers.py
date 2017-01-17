from bs4 import BeautifulSoup

from crawler.parsers import parse_offer


def load_fixture(filename):
    with open("tests/fixtures/%s" % filename, 'r') as f:
        content = "".join(f.readlines())
        return BeautifulSoup(content, 'html.parser').find()


class TestParseOffer:
    url_offer_1 = 'https://www.otomoto.pl/oferta/audi-a6-avant-2-0-tdi-ultra-190-km-2015-czarny-bezwypadek-ID6yEEct.html#10c7404c66'
    url_offer_2 = 'https://www.otomoto.pl/oferta/bmw-x1-sdrive18d-advantage-2-0-d-150-km-2015r-premium-selection-ID6yEmJT.html#10c7404c66'
    url_dealer_1 = 'https://ciesielczyk.otomoto.pl'

    def test_listing_promoted(self):
        fixture = load_fixture('listing_promoted.html')
        print(type(fixture))
        offer = parse_offer(fixture)

        assert 'Audi A6 C7' == offer['title']
        assert '6008880069' == offer['id']
        assert self.url_offer_1 == offer['url']
        assert offer['promoted'] is True
        assert 'dealer' not in offer

    def test_listing_promoted_from_dealer_plus(self):
        fixture = load_fixture('listing_promoted_dealer_plus.html')
        print(type(fixture))
        offer = parse_offer(fixture)

        assert 'BMW X1 F48' == offer['title']
        assert '6008812949' == offer['id']
        assert self.url_offer_2 == offer['url']
        assert offer['promoted'] is True
        assert 'dealer' in offer
        assert self.url_dealer_1 == offer['dealer']
