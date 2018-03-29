import os
from config import Config
import time
import notify2
import logging
from plugins.gmail.gmail import GmailFeed
from plugins.rss.rss import RSS_Feed


logger = logging.getLogger("AReader")  # init logger


def main():
    # globals
    CONFIG = Config()
    PROVIDERS = {
        "gmail": GmailFeed,
        "rss": RSS_Feed
    }
    FEEDS = []
    SLEEP_TIME = 10
    # load providers
    for feed in CONFIG.get("feeds"):
        provider_name = feed['provider']
        if provider_name not in PROVIDERS.keys():
            logger.error("PROVIDER NOT FOUND: " + provider_name)
            return
        provider = PROVIDERS[provider_name](feed)
        feed = provider.get_config()
        CONFIG.write()
        FEEDS.append(provider)
    # init notification
    notify2.init("AReader")
    while True:
        for feed in FEEDS:
            try:
                notif = feed.get_notification()
                if notif:
                    n = notify2.Notification(*notif)
                    n.show()
            except Exception:
                print("error on {}".format(feed))
        time.sleep(SLEEP_TIME)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nGood Bye!")
        pass
