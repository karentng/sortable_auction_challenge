import json
import logging

from auction.models import Site, Bid
CONFIG_FILE = "/auction/config.json"


def load_configs():
    """
    Load all sites and biders from the config file.

    :return: configurations loaded
    :rtype list sites: list of sites objects with name, bidders and floor attribute
    :rtype dict adjustments: dictionary with the bidder id as key and adjustment as value
    """
    with open(CONFIG_FILE, encoding="utf-8") as json_data:
        config = json.load(json_data)

    sites = config["sites"]
    sites_objects = {}
    bidders = config["bidders"]
    adjustments = {}

    for site_dict in sites:
        new_site = Site(site_dict)
        sites_objects[new_site.name] = new_site

    for bidder in bidders:
        adjustments[bidder["name"]] = bidder["adjustment"]

    logging.info(f"All config loaded: sites {len(sites)}, bidders {len(bidders)}")
    return sites_objects, adjustments


def process_auctions(sites_dict, adjustments, auctions):
    """
    Runs all auctions ang after validation, gets the winners

    :param dict sites_dict:
    :param dict adjustments:
    :param auctions:
    :return: result of processing every auction input
    :rtype list[list[bids]] auctions_results: list of list with the winner bids represented by a dictionary
    """
    auctions_results = []
    for auction in auctions:
        auction_site = auction["site"]
        winning_bids = []
        # if auction site is not recognized will add an empty list as result and process the next one
        if auction_site not in sites_dict:
            auctions_results.append(winning_bids)
            logging.info(f"Ignoring auction for unrecognized site: {auction_site}")
            continue

        site_obj = sites_dict[auction_site]
        units = auction["units"]
        valid_bids = get_valid_bids(auction["bids"], site_obj, adjustments, units)
        # if there is no valid bid the auction will have an empty list as result
        winning_bids = get_winning_bids(valid_bids, site_obj.floor, adjustments) if valid_bids else []
        auctions_results.append(winning_bids)

    logging.info(f"All auctions processed")
    return auctions_results


def get_valid_bids(bids, site, adjustments, units):
    """
    Validates a list of bids, filtering the invalid ones

    :param list bids:
    :param models.Site site: object that corresponds to the site for the list of bids to process
    :param dict adjustments: dictionary for mapping bidders to adjustment
    :param list units: list of valid units to bid in the auction
    :return: valid bids organized by unit
    :rtype dict valid_bidders: dictionary with unit as key and the list of valid bids on that unit as value
    """
    valid_bidders = {unit: [] for unit in units}
    for bid in bids:
        bidder = bid["bidder"]
        unit = bid["unit"]
        # invalid bid: bidder not allowed in site, bidder unknown, unit not allowed in the auction
        if bidder not in site.bidders and bidder not in adjustments and unit not in units:
            logging.info(f"Ignoring invalid bid{bid}")
            continue

        new_bid = Bid(bid)
        valid_bidders[unit].append(new_bid)  # adds the bid to a list dictionary of valid bids

    logging.info(f"Finished bids validation")
    return valid_bidders


def get_winning_bids(bids_by_unit, floor, adjustments):
    """
    Gets the list of winners in all units

    :param dict bids_by_unit: list of bids organized by units: unit:[valid_bids]
    :param float floor: The site's floors value
    :param dict adjustments: the key is the bidder and as value the respective adjustment loaded in config
    :return: list of winner bids on all units
    :rtype list winning_bids: list of winner bids. Each bid is represented as a dictionary
    """
    winning_bids = []
    for bids in bids_by_unit:
        # gets the winner bid from a list of bids per unit and appends in a list of winners
        winner_in_unit = get_winner_by_unit(bids_by_unit[bids], floor, adjustments)
        winning_bids.append(winner_in_unit.__dict__) if winner_in_unit else None

    logging.info(f"All winner bids processed")
    return winning_bids


def get_winner_by_unit(bids_by_unit, floor, adjustments):
    """
    Gets the winner bid in a specific unit

    :param list bids_by_unit: all valid bids in tha unit to get the winner from
    :param float floor: The site's floors value
    :param dict adjustments: the key is the bidder and as value the respective adjustment loaded in config
    :return: the bid winner in a unit
    :rtype models.Bid: Object Bid
    """
    winner_bid = None
    winner_index = None

    for index in range(0, len(bids_by_unit)):
        bid = bids_by_unit[index]
        real_bid = get_adjusted_bid(bid.bid, adjustments[bid.bidder])
        # the bid is ignored when the real bid is less than the site's floor
        if real_bid < floor:
            logging.info(f"Ignoring invalid bid {{{bid.bidder}, {bid.bid}, {bid.unit}}} does not exceed floor {floor}")
            continue

        if not winner_bid or winner_bid < real_bid:
            winner_index = index
            winner_bid = real_bid

    logging.info(f"Unit processed to find winner")

    if winner_index is None:
        logging.info(f"Valid bid not found. It will return empty list")
        return

    # after iterating over all bids, winner_index holds the index to access the maximum bid in the unit's list
    return bids_by_unit[winner_index]


def get_adjusted_bid(bid, adjustment):
    """
    Calculates the real bit with the bidder adjustment

    :param float bid: the bid value
    :param float adjustment: adjustment value to get the real bid
    :return: represents the actual value to pay by the bidder after adjustment
    :rtype float real_bid: float with the real value of a bid
    """
    real_bid = bid + (bid * adjustment)
    logging.info(f"Getting ajusted bid {real_bid}")
    return real_bid





