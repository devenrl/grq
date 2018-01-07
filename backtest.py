import argparse
import importlib


def main():
    aparser = argparse.ArgumentParser()
    aparser.add_argument("history")
    aparser.add_argument("predictor")
    args = aparser.parse_args()

    # Read in the test data
    data = read_history(args.history)

    # Import the brain
    brain = importlib.import_module(args.predictor)

    # Concat into one big list and sort by time
    unified_feed = []
    for product_name in brain.REQUIRED_PRODUCTS:
        unified_feed.extend(data[product_name])
    sorted_feed = sorted(unified_feed, key=lambda x: x[1])
    print "Final feed length:", len(sorted_feed)

    # Initialize some random starting values:
    brain.USD = 1000
    brain.BTC = 0
    brain.ETH = 0

    for tick in sorted_feed:
        brain.send_tick(tick)

    print "final value:", brain.final_value()

    # for f in brain.change_rates:
    #     print f


def read_history(fn):
    with open(fn, "r") as ifile:
        data = ifile.read()

    lines = [x.split("\t") for x in data.split("\n")][:-1]

    products = set([x[0] for x in lines])

    by_product = {}
    for product in products:
        by_product[product] = [x for x in lines if x[0] == product]

    return by_product


if __name__ == '__main__':
    main()
