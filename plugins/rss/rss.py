import feedparser


class RSS_Feed():
    def __init__(self, feed):
        self.feed = feed
        print("Init RSS_Feed")
        return

    def get_config(self):
        return self.feed

    def get_notification(self):
        req = feedparser.parse(self.feed["url"])
        title = req["feed"]["title"]
        if "title" in self.feed:
            title = self.feed["title"]
        update = req['feed']['updated_parsed']
        if 'last_update' in self.feed:
            if self.feed["last_update"] == update:
                return
            req["entries"] = [x for x in req["entries"]
                              if x["updated_parsed"] > self.feed["last_update"]]
        self.feed['last_update'] = update
        num = len(req['entries'])
        if num == 0:
            return
        if num == 1:
            entry = req['entries'][0]
            msg = entry['title']
        else:
            msg = "{} new entries".format(num)
        return (title, msg)