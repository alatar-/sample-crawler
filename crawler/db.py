def store_offer(offer, db):
    dealer = offer.pop('dealer')
    offer_id = offer.pop('id')

    if not db.get('dealer', None):
        db[dealer] = {}

    db[dealer][offer_id] = offer
