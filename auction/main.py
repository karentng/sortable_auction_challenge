import json
import logging
import sys

from auction.run_auctions import load_configs, process_auctions


def main():
    """
    Main function to load configurations and process the input file
    """
    # uncomment the line below to see logs
    # logging.basicConfig(level=logging.INFO)
    sites, adjustments = load_configs()
    auctions = json.load(sys.stdin)
    winners_auctions = process_auctions(sites, adjustments, auctions)
    print(json.dumps(winners_auctions, indent=4, sort_keys=True))


if __name__ == "__main__":
    main()
