import json
import sys

class Config:
    def __init__(self, sites, adjustments):
        self.sites = sites
        self.adjustments = adjustments
        
def load_config(config_path):
    with open(config_path) as f:
        sites = {}
        adjustments = {}
        config = json.load(f)
        for site in config["sites"]:
            sites[site["name"]] = site
        for bidder in config["bidders"]:
            adjustments[bidder["name"]] = bidder["adjustment"]
        return Config(sites,adjustments)

def adjusted_bid(bid, config):
    return (config.adjustments[bid["bidder"]] + 1) * bid["bid"]
    
def run_auction(auction, config):
    if auction["site"] not in config.sites:
        return []
    site_config = config.sites[auction["site"]]
    winner={}
    for bid in auction["bids"]:
        bidder = bid["bidder"]
        if bidder not in site_config["bidders"]:
            continue
        unit = bid["unit"]
        if unit not in auction["units"]:
            continue
        amount = adjusted_bid(bid, config)
        if amount < site_config["floor"]:
            continue
        if not unit in winner or amount > adjusted_bid(winner[unit], config):
            winner[unit]=bid
    res=[]
    for bid in winner.values():
        res.append(bid)
    return res

def main():
    config = load_config("/auction/config.json")
    input_str = sys.stdin.read()
    auctions = json.loads(input_str)
    res = []
    for auction in auctions:
        res.append(run_auction(auction, config))
    print(json.dumps(res))
    
if __name__ == "__main__":
    main()
