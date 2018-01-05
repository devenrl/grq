import gdax
import time
import boto3
import traceback


class myWebsocketClient(gdax.WebsocketClient):
    def on_open(self):
        # self.url = "wss://ws-feed.gdax.com/"
        self.products = ["BTC-USD", "ETH-USD", "ETH-BTC", "LTC-BTC", "LTC-USD"]
        self.channels = ['ticker']
        self.message_count = 0
        self.dyn_client = boto3.client('dynamodb')
        print("Lets count the messages!")

    def on_message(self, msg):
        self.message_count += 1
        if msg['type'] == 'ticker' and 'time' in msg:
            print msg['price']
            try:
                self.dyn_client.put_item(
                    TableName="tickers",
                    Item={
                        'uid': {
                            'S': "{}-{}".format(msg['product_id'], msg['sequence'])
                        },
                        'time': {
                            'S': msg['time']
                        },
                        'product_id': {
                            'S': msg['product_id']
                        },
                        'price': {
                            'N': msg['price']
                        }
                    })
            except:
                traceback.print_exc()

    def on_close(self):
        print("-- Goodbye! --")


def main():
    wsClient = myWebsocketClient()
    wsClient.start()
    print(wsClient.url, wsClient.products)
    while True:
        time.sleep(10)
    wsClient.close()


if __name__ == '__main__':
    main()
