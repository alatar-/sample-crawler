import shelve

from .config import db_filename


class PseudoDB:
    db = None

    def __init__(self, filename=db_filename):
        self.filename = filename

    def __enter__(self):
        self.db = shelve.open(self.filename)
        return self

    def __exit__(self, *args):
        self.db.close()

    def store_offer(self, offer):
        dealer = offer.pop('dealer')
        offer_id = offer.pop('id')

        if not self.db.get('dealer', None):
            self.db[dealer] = {}

        self.db[dealer][offer_id] = offer
