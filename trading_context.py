

class TradingContext(object):
	def __init__(self, currency_pairs, tax):
		self.currency_pairs = []
		# All current pairs that can trade on this exchange
		self.tax = tax


Gdax = TradingContext(
	["ETH-BTC", "ETH-USD", "LTC-USD", "BTC-USD", "LTC-BTC"],
	0.0)

