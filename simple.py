from datetime import datetime
# ETH-BTC
# ETH-USD
# LTC-USD
# BTC-USD
# LTC-BTC

REQUIRED_PRODUCTS = [
    'ETH-BTC',
    'BTC-USD',
    'ETH-USD'
]

USD = 0
BTC = 0
ETH = 0

eth_btc = None
eth_btc_0 = None
btc_usd = None
btc_usd_0 = None
eth_usd = None
eth_usd_0 = None
price_history = []
change_rates = []

all_in = "USD"


def trade(product, action, quantity, price):
    '''
    This stub function is to be replaced by either a real trading engine
    or a testing one
    '''
    global USD, BTC, ETH
    # print
    # Just assume the trade goes through at the current price?
    if product == 'BTC-USD':
        if action == 'buy':
            USD -= quantity * price
            BTC += quantity
            print "BOUGHT SOME BTC WITH USD"

        elif action == 'sell':
            BTC -= quantity
            USD += quantity * price
            print "SOLD SOME BTC FOR USD"

    elif product == 'ETH-USD':
        if action == 'buy':
            USD -= quantity * price
            ETH += quantity
            print "BOUGHT SOME ETH WITH USD"

        elif action == 'sell':
            ETH -= quantity
            USD += quantity * price
            print "SOLD SOME ETH FOR USD"

    elif product == 'ETH-BTC':
        if action == 'buy':
            BTC -= quantity * price
            ETH += quantity
            print "BOUGHT SOME ETH USING BTC"

        elif action == 'sell':
            ETH -= quantity
            BTC += quantity * price
            print "SOLD SOME ETH FOR BTC"

    if USD < 0.00000001:
        USD = 0
    if BTC < 0.00000001:
        BTC = 0
    if ETH < 0.00000001:
        ETH = 0

    print "NEW BALANCES:", USD, BTC, ETH


def send_tick(tick):
    '''
    This function will be called with every new tick of the ticker!
    '''
    global eth_btc, btc_usd, eth_usd
    global eth_btc_0, btc_usd_0, eth_usd_0
    global price_history, change_rates
    global all_in
    product_id, time, price = tick
    price = float(price)

    # First, update some state:
    if product_id == 'ETH-BTC':
        eth_btc_0 = eth_btc
        eth_btc = price

    elif product_id == 'BTC-USD':
        btc_usd_0 = btc_usd
        btc_usd = price

    elif product_id == 'ETH-USD':
        eth_usd_0 = eth_usd
        eth_usd = price

    # If we don't even have complete information yet, do nothing
    if eth_btc_0 is None or btc_usd_0 is None or eth_usd_0 is None:
        return

    # We need to check: has more time elapsed than the window?
    # If so, we need to save all these prices and then create a new window
    time_object = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%fZ")

    if len(price_history) == 0:
        # First time through. Save everything
        price_history.append((time_object, btc_usd_0, eth_usd_0, eth_btc_0))

    else:
        last_recorded_time = price_history[-1][0]
        delta_t = (time_object - last_recorded_time).total_seconds()
        # print delta_t

        if delta_t > 60:
            # print "window"
            price_history.append((time_object, btc_usd_0, eth_usd_0, eth_btc_0))

            # calculate change rates!
            before = price_history[-2]
            after = price_history[-1]

            change_rates.append((
                after[1] / before[1],
                after[2] / before[2]))
                # after[3] / before[3]))

            # COR:
            # Whatever happened last timestep will continue to this time step!
            rates = change_rates[-1]
            # rates = [1 / x for x in rates]

            # Which of those rates is highest?
            best_index = rates.index(max(rates))

            # Go all in on that!
            if best_index == 0:
                all_in = "BTC"
            elif best_index == 1:
                all_in = "ETH"

            # sell means move -->
            # buy means move <--

            # ALL IN!
            if all_in == "BTC":
                if USD > 0:
                    trade('BTC-USD', 'buy', USD / btc_usd, btc_usd)  # ?
                if ETH > 0:
                    trade('ETH-BTC', 'sell', ETH, eth_btc)   # GOOD

            # elif all_in == "USD":
            #     if BTC > 0:
            #         trade('BTC-USD', 'sell', BTC, btc_usd)
            #     if ETH > 0:
            #         trade('ETH-USD', 'sell', ETH, eth_btc)

            if all_in == "ETH":
                if USD > 0:
                    trade('ETH-USD', 'buy', USD / eth_usd, eth_usd)  # GOOD
                if BTC > 0:
                    trade('ETH-BTC', 'buy', BTC / eth_btc, eth_btc)   # GOOD

    # ANTI-COR


def final_value():
    '''
    only used at the end of backtesting, to see how well it did
    '''
    # Just convert it all to USD
    return USD + BTC * btc_usd + ETH * eth_usd
