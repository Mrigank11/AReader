import feedparser
import time
import webbrowser
import re


class RSS_Feed():
    def __init__(self, feed):
        self.feed = feed
        print("Init RSS_Feed")
        return

    def fix_time(self, t):
        return time.strftime("%Y-%m-%dT%H:%M:%S", t)

    def handle_notification_callback(self, n, action, data=None):
        if data:
            webbrowser.open(data)
            return

        if "homepage" in self.feed:
            webbrowser.open(self.feed["homepage"])
        else:
            # try to guess homepage
            try:
                homepage = re.match(r"(http.?://.*?/)",
                                    self.feed["url"]).group(1)
                webbrowser.open(homepage)
            except Exception:
                print("unable to get homepage")

    def get_notification(self):
        req = feedparser.parse(self.feed["url"])
        title = req["feed"]["title"]
        if "title" in self.feed:
            title = self.feed["title"]
        update = self.fix_time(req['feed']['updated_parsed'])
        if 'last_update' in self.feed:
            if self.feed["last_update"] == update:
                return
            req["entries"] = [x for x in req["entries"]
                              if self.fix_time(x["updated_parsed"]) > self.feed["last_update"]]
        self.feed['last_update'] = update
        num = len(req['entries'])
        if num == 0:
            return
        if num == 1:
            entry = req['entries'][0]
            msg = entry['title']
            data = entry['link']
        else:
            msg = "{} new entries".format(num)
            data = None
        return (title, msg, "", data, self.handle_notification_callback)
