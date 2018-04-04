from config import Config
import time
import logging
from threading import Thread
from plugins.gmail.gmail import GmailFeed
from plugins.rss.rss import RSS_Feed
from notifier import Notifier


logger = logging.getLogger("AReader")  # init logger

# globals
CONFIG = Config()
PROVIDERS = {
    "gmail": GmailFeed,
    "rss": RSS_Feed
}
SLEEP_TIME = 20
NOTIFICATION_TIMEOUT = 5000
NOTIFIER = Notifier(NOTIFICATION_TIMEOUT)


def main():
    FEEDS = []
    THREADS = []
    # load providers
    for feed in CONFIG.get("feeds"):
        provider_name = feed['provider']
        if provider_name not in PROVIDERS.keys():
            logger.error("PROVIDER NOT FOUND: " + provider_name)
            return
        provider = PROVIDERS[provider_name](feed)
        provider.last_checked = None
        # feed obj might have changed, update config
        CONFIG.write()
        FEEDS.append(provider)

    def handle_feed(feed):
        try:
            notif = feed.get_notification()
            feed.last_checked = time.strftime("%H:%M:%S", time.localtime())
            # feed obj might have changed, update config
            CONFIG.write()
            if notif:
                NOTIFIER.notify(*notif)
        except Exception as e:
            print("error on {}: {}".format(feed, e))

    while True:
        for th in THREADS:
            th.join()
        THREADS = []
        print("\r", end="")
        for feed in FEEDS:
            print(feed.feed['provider'], feed.last_checked, end=" ")
            t = Thread(target=handle_feed, args=(feed,))
            t.start()
            THREADS.append(t)
        time.sleep(SLEEP_TIME)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nGood Bye!")
        NOTIFIER.close()
        exit(0)
