
import gdax
import time


class myWebsocketClient(gdax.WebsocketClient):
    # def __init__(self, *args, **kwargs):
    #     super(myWebsocketClient, self).__init__(*args, **kwargs)

    def on_open(self):
        self.url = "wss://ws-feed.gdax.com/"
        self.products = ["LTC-USD"]
        self.channels = "match"
        self.message_count = 0
        print("Lets count the messages!")

    def on_message(self, msg):
        self.message_count += 1
        if msg['type'] == 'match':
            print msg
        # if 'price' in msg and 'type' in msg:
            # print("Message type:", msg["type"],
            #       "\t@ {:.3f}".format(float(msg["price"])))

    def on_close(self):
        print("-- Goodbye! --")


def main():
    wsClient = myWebsocketClient()
    wsClient.start()
    print(wsClient.url, wsClient.products)
    count = 0
    while count < 10:
        # print("\nmessage_count =", "{} \n".format(wsClient.message_count))
        time.sleep(1)
        count += 1
    wsClient.close()


if __name__ == '__main__':
    main()
