

# buy and hold
# Market (Universal BAH)
# Best stock
# CBAL (constant rebalancing)
# UCBAL
# uniform constant rebalance
#
# Metrics:
# accumulated wealth
# annualized return
# hit rate (fraction of trades with profitable returns)
# average return per trading period
# standard deviation of returns
# downside standard deviation of returns
# sharpe ratio
# sterling ratio
# sortino ratio
# calmar ratio
# burke ratio
# omega ratio (for r = 0, and for r = cost of money)
# maximum downdraw ratio
# risk return ratio
#
from algorithms import BuyAndHold


def read_history(fn):
    with open(fn, "r") as ifile:
        data = ifile.read()

    lines = [x.split("\t") for x in data.split("\n")][:-1]

    lines = sorted(lines, key=lambda x: x[1])

    return lines


class User(object):
    def __init__(self, cash):
        self.assets = {
            "USD": cash
        }

    def init_assets(self, exchange):
        for p in exchange.products:
            if p['name'] not in self.assets.keys():
                self.assets[p['buy']] = 0

    def algorithm(self):
        raise ("OOPS! You haven't supplied an algorithm!")



class Exchange(object):
    def __init__(self, products):
        self.products = products
        for p in products:
            buy, buy_with = p['name'].split("-")
            p['buy'] = buy
            p['buy_with'] = buy_with

        self.product_names = [p['name'] for p in self.products]
        self.current_prices = {}


    def process_tick(self, tick):
        product_id, time, price = tick

        # update our version of "most recent price"
        self.current_prices[product_id] = float(price)


    def market_order(self, user, product_id, action, amount):
        '''
        action is either 'buy' or 'sell'
        '''
        latest_price = self.current_prices[product_id]

        if action == 'buy':
            buy, buy_with = product_id.split("-")
        elif action == 'sell':
            buy_with, buy = product_id.split("-")

        if user.assets[buy_with] < amount:
            print "Order rejected! Insufficient funds!"
            return

        # Great, make the exchange at the latest price!
        user.assets[buy_with] -= amount
        user.assets[buy] += amount / latest_price


    def limit_order(self, user, action, amount, price):
        pass


    def stop_order(self, user, action, amount, price):
        pass


    def process_order(self, user, order):
        product_id, order_type, action, amount, price = order
        print order

        if order_type == 'market':
            self.market_order(user, product_id, action, amount)

        elif order_type == "limit":
            self.limit_order(user, product_id, action, amount, price)

        elif order_type == 'stop':
            self.stop_order(user, product_id, action, amount, price)

    def value_assets(self, assets, target_currency="USD"):
        value = 0
        for name, amount in assets.iteritems():

            if name == target_currency:
                value += amount
                continue

            # Assumption: on this exchange, every asset
            # can be directly converted to the target currency
            product_id = "{}-{}".format(name, target_currency)

            latest_price = self.current_prices[product_id]

            value += amount * latest_price

        return value


GDAX = Exchange(
    [
        {
            "name": "BTC-USD",
            "tax:": 0.0
        },
        {
            "name": "ETH-USD",
            "tax:": 0.0
        },
        {
            "name": "LTC-USD",
            "tax:": 0.0
        },
        {
            "name": "ETH-BTC",
            "tax:": 0.0
        },
        {
            "name": "LTC-BTC",
            "tax:": 0.0
        }
    ])

def run_algorithm(user, algo, history, exchange):
    for tick in history:
        exchange.process_tick(tick)
        orders = algo.process_tick(tick)

        for order in orders:
            exchange.process_order(user, order)


def calculate_metrics(user, algo, history, exchange, target_currency="USD"):
    # Total final value in USD
    usd_value = exchange.value_assets(user.assets, target_currency)

    return {
        'total_value': usd_value
    }


def main():
    matt = User(cash=1000)
    matt.init_assets(GDAX)

    history = read_history("history.csv")
    print len(history)

    algo = BuyAndHold(matt, "LTC", GDAX)

    run_algorithm(matt, algo, history, GDAX)
    metrics = calculate_metrics(matt, algo, history, GDAX)

    print "Metrics:"
    print metrics

if __name__ == '__main__':
    main()
