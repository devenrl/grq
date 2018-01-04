import gdax
import time


class myWebsocketClient(gdax.WebsocketClient):
    def on_open(self):
        self.url = "wss://ws-feed.gdax.com/"
        self.products = ["LTC-USD"]
        self.channels = "match"
        self.message_count = 0
        print("Lets count the messages!")

    def on_message(self, msg):
        self.message_count += 1
        if msg['type'] == 'match':

            minimal = {
                'price': msg['price'],
                'time': msg['time'],
                'side': msg['side'],
                'size': msg['size'],
            }
            print minimal

    def on_close(self):
        print("-- Goodbye! --")


def main():
    wsClient = myWebsocketClient()
    wsClient.start()
    print(wsClient.url, wsClient.products)
    count = 0
    while count < 10:
        time.sleep(1)
        count += 1
    wsClient.close()


if __name__ == '__main__':
    main()
