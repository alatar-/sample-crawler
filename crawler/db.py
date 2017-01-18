import shelve

from .config import db_filename


class PseudoDB:
    '''Scheme (object-value):
        dealer(id-url): <set> offer(id)
        offer(id): <dict> properties(title, url, ...)
    '''
    dealers = None
    offers = None

    def __init__(self, filename=db_filename):
        self.__filename = filename

    def __enter__(self):
        self.__db = shelve.open(self.__filename, writeback=True)
        if 'dealers' not in self.__db:
            self.__db['dealers'] = {}

        if 'offers' not in self.__db:
            self.__db['offers'] = {}

        self.dealers = self.__db['dealers']
        self.offers = self.__db['offers']
        return self

    def __exit__(self, *args):
        self.__db.close()

    def store_offer(self, offer):
        dealer = offer['dealer']
        offer_id = offer.pop('id')

        if dealer not in self.dealers:
            self.dealers[dealer] = set()
        self.dealers[dealer].add(offer_id)
        self.offers[offer_id] = offer

    def get_dealer_offers(self, dealer):
        return self.dealers[dealer]

    def get_dealers(self):
        return self.dealers.keys()

    def get_offers_gen(self):
        for offer_id in self.offers:
            yield offer_id

    def drop_offer(self, offer_id):
        offer = self.offers.pop(offer_id)
        dealer = offer['dealer']
        self.dealers[dealer].remove(offer_id)

        return offer
