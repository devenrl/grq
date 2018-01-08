

class TradingAlgo(object):
    def __init__(self, exchange, user, window_seconds):
        self.trade_history = []
        self.asset_history = []
        self.ticker_history = {}
        self.current_prices = {}
        self.old_prices = {}
        self.user = user
        self.window_seconds = window_seconds
        self.buyables = list(set([p['buy'] for p in exchange.products]))
        self.exchange = exchange

        products = [p['name'] for p in exchange.products]

        for p in products:
            self.old_prices[p] = None
            self.current_prices[p] = None

    def process_tick(self, tick):
        product_id, time, price = tick

        # First, just make sure we remember this tick
        if product_id not in self.ticker_history.keys():
            self.ticker_history[product_id] = []
        self.ticker_history[product_id].append((time, price))


        # Also, update our version of "most recent price"
        self.old_prices[product_id] = self.current_prices[product_id]
        self.current_prices[product_id] = price


class BuyAndHold(TradingAlgo):
    def __init__(self, user, desired_currency, exchange, window_seconds=60):
        super(BuyAndHold, self).__init__(exchange, user, window_seconds)

        self.desired_currency = desired_currency


    def process_tick(self, tick):
        super(BuyAndHold, self).process_tick(tick)
        orders = []

        # Well..don't do anything until I have at least one price for
        # each asset on the market

        if None in self.current_prices.values():
            return []

        # What does this user have that is not the target currency?
        for asset_name, amount in self.user.assets.iteritems():
            if amount > 0 and asset_name != self.desired_currency:
                # Well...check if we can make a direct exchange!
                desired_exchange_name = "{}-{}".format(
                    self.desired_currency, asset_name)

                if desired_exchange_name in self.exchange.product_names:
                    # sweet! just place a buy order!
                    orders.append((
                        desired_exchange_name, 'market', 'buy', amount, None))
                    continue

                # damn well...maybe the exchange just has the opposite name?
                desired_exchange_name_rev = "{}-{}".format(
                    asset_name, self.desired_currency)

                if desired_exchange_name_rev in self.exchange.product_names:
                    # sweet! just place a sell order!
                    orders.append((
                        desired_exchange_name_rev, 'market', 'sell', amount, None))
                    continue

        return orders

