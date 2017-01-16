def parse_offer(l):
    offer = {}
    offer['promoted'] = 'promoted' in l['class']

    l_a = l.find('h2', 'offer-title').a
    offer['title'] = l_a.get_text().strip()
    offer['id'] = l_a['data-ad-id']
    offer['url'] = l_a['href']

    l_d = l.find('div', 'seller-logo')
    if l_d is not None:
        offer['dealer-url'] = l_d.a['href']
    
    return offer
