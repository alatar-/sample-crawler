from bs4 import BeautifulSoup

from crawler.parsers import *


def load_fixture(filename):
    with open("tests/fixtures/%s" % filename, 'r') as f:
        content = "".join(f.readlines())
        return BeautifulSoup(content, 'html.parser').find()


class TestTranslateTimestamp:

    def test_timestamp_1(self):
        fixture = "05:53, 17 stycznia 2017"
        ts = translate_timestamp(fixture)

        ts_expected = datetime.datetime(2017, 1, 17, 5, 53)
        assert ts_expected == ts


class TestParseOfferPage:
    url_dealer = 'https://bmw-olszowiec.otomoto.pl'

    def test_timestamp(self):
        fixture = load_fixture('offer_page.html')
        offer = {}
        offer = parse_offer_page(fixture, offer)

        ts_expected = datetime.datetime(2017, 1, 17, 5, 53)
        assert ts_expected == offer['timestamp']

    def test_dealer(self):
        fixture = load_fixture('offer_page.html')
        offer = {}
        offer = parse_offer_page(fixture, offer)

        assert self.url_dealer == offer['dealer']


class TestGetNextPageUrl:
    next_page_url = 'https://www.otomoto.pl/osobowe/poznan/?search%5Bfilter_enum_authorized_dealer%5D=1&search%5Bdist%5D=50&search%5Bcountry%5D=&page=4'

    def test_next_url(self):
        fixture = load_fixture('catalog_middle_page.html')
        result = get_next_page_url(fixture)

        assert self.next_page_url == result

    def test_doesnt_exist(self):
        fixture = load_fixture('catalog_last_page.html')
        result = get_next_page_url(fixture)

        assert result is None


class TestParseCatalogListing:
    url_offer_1 = 'https://www.otomoto.pl/oferta/audi-a6-avant-2-0-tdi-ultra-190-km-2015-czarny-bezwypadek-ID6yEEct.html#10c7404c66'
    url_offer_2 = 'https://www.otomoto.pl/oferta/bmw-x1-sdrive18d-advantage-2-0-d-150-km-2015r-premium-selection-ID6yEmJT.html#10c7404c66'
    url_dealer_1 = 'https://ciesielczyk.otomoto.pl'

    def test_general_info(self):
        fixture = load_fixture('listing_promoted.html')
        offer = parse_catalog_listing(fixture)

        assert 'Audi A6 C7' == offer['title']
        assert '6008880069' == offer['id']
        assert self.url_offer_1 == offer['url']

    def test_general_info_2(self):
        fixture = load_fixture('listing_promoted_dealer_plus.html')
        offer = parse_catalog_listing(fixture)

        assert 'BMW X1 F48' == offer['title']
        assert '6008812949' == offer['id']
        assert self.url_offer_2 == offer['url']
        assert offer['promoted'] is True

    def test_no_dealer_info(self):
        fixture = load_fixture('listing_promoted.html')
        offer = parse_catalog_listing(fixture)

        assert 'dealer' not in offer

    def test_promoted(self):
        fixture = load_fixture('listing_promoted.html')
        offer = parse_catalog_listing(fixture)

        assert offer['promoted'] is True

    def test_from_dealer_plus(self):
        fixture = load_fixture('listing_promoted_dealer_plus.html')
        offer = parse_catalog_listing(fixture)

        assert 'dealer' in offer
        assert self.url_dealer_1 == offer['dealer']
