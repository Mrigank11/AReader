import os
from config import Config
import time
import notify2
import logging
from plugins.gmail.gmail import GmailFeed
from plugins.rss.rss import RSS_Feed

from threading import Thread

logger = logging.getLogger("AReader")  # init logger


def main():
    # globals
    CONFIG = Config()
    PROVIDERS = {
        "gmail": GmailFeed,
        "rss": RSS_Feed
    }
    FEEDS = []
    THREADS = []
    SLEEP_TIME = 10
    # load providers
    for feed in CONFIG.get("feeds"):
        provider_name = feed['provider']
        if provider_name not in PROVIDERS.keys():
            logger.error("PROVIDER NOT FOUND: " + provider_name)
            return
        provider = PROVIDERS[provider_name](feed)
        # feed obj might have changed, update config
        CONFIG.write()
        FEEDS.append(provider)

    def handle_feed(feed):
        try:
            notif = feed.get_notification()
            # feed obj might have changed, update config
            CONFIG.write()
            if notif:
                n = notify2.Notification(*notif)
                n.show()
        except Exception as e:
            print("error on {}: {}".format(feed, e))

    # init notification
    notify2.init("AReader")
    while True:
        for th in THREADS:
            th.join()
        THREADS = []
        for feed in FEEDS:
            t = Thread(target=handle_feed, args=(feed,))
            t.start()
            THREADS.append(t)
        time.sleep(SLEEP_TIME)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nGood Bye!")
