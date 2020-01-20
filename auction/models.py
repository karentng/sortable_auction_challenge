class Bid:
    bidder = None
    bid = None
    unit = None

    def __init__(self, bid):
        self.bidder = bid["bidder"]
        self.bid = bid["bid"]
        self.unit = bid["unit"]


class Site:
    name = None
    bidders = None
    floor = None

    def __init__(self, site):
        self.name = site["name"]
        self. bidders = site["bidders"]
        self.floor = site["floor"]

