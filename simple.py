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


def trade(product, action, quantity, price):
    '''
    This stub function is to be replaced by either a real trading engine
    or a testing one
    '''
    global USD, BTC, ETH
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


def send_tick(tick):
    '''
    This function will be called with every new tick of the ticker!
    '''
    global eth_btc, btc_usd, eth_usd
    global eth_btc_0, btc_usd_0, eth_usd_0
    global price_history
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
            print "window"
            price_history.append((time_object, btc_usd_0, eth_usd_0, eth_btc_0))

    # Put it all in BTC!
    if USD > 0:
        trade('BTC-USD', 'buy', USD / btc_usd, btc_usd)
    if ETH > 0:
        trade('ETH-BTC', 'sell', ETH * eth_btc, eth_btc)


    # # Put it all in BTC!
    # if USD > 0:
    #     trade('BTC-USD', 'buy', USD / btc_usd, btc_usd)
    # if ETH > 0:
    #     trade('ETH-BTC', ETH)


def final_value():
    '''
    only used at the end of backtesting, to see how well it did
    '''
    # Just convert it all to USD
    return USD + BTC * btc_usd + ETH * eth_usd
