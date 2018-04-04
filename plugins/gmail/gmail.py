import feedparser
from google.auth.transport.requests import AuthorizedSession
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import time
import webbrowser
import re


class GmailFeed():
    def __init__(self, feed):
        self.feed = feed
        print("Init Gmail")
        # try to validate feed
        if("creds" not in self.feed):
            # start server and get token
            print("token not found")
            self.flow = InstalledAppFlow.from_client_secrets_file(
                'plugins/gmail/client_secret.json',
                scopes=['https://mail.google.com/mail/feed/atom'])
            self.flow.run_local_server(
                port=8888, open_browser=True, access_type='offline', include_granted_scopes='true', prompt='consent')
            self.save_creds()
            # hack to prevent server from crashing due to chrome requesting /favicon.ico
            time.sleep(5)
        else:
            self.get_session()

    def get_session(self):
        creds = Credentials(** self.feed["creds"])
        self.session = AuthorizedSession(creds)

    def save_creds(self):
        credentials = self.flow.credentials
        creds = {'token': credentials.token,
                 'refresh_token': credentials.refresh_token,
                 'token_uri': credentials.token_uri,
                 'client_id': credentials.client_id,
                 'client_secret': credentials.client_secret,
                 'scopes': credentials.scopes}
        self.feed['creds'] = creds
        self.get_session()
        return self.feed

    def handle_notification_callback(self, n, action, data):
        print("Opening in gmail")
        link = data or "https://mail.google.com/mail"
        # change user index
        if 'u' in self.feed:
            link = re.sub(r"google.com/mail(/u/.)?",
                          "google.com/mail/u/" + self.feed['u'], link)
        # open browser
        webbrowser.open(link)

    def get_notification(self):
        title = "Gmail"
        label = ""
        if 'label' in self.feed:
            label = self.feed['label']
        if 'alias' in self.feed:
            title = self.feed['alias']
        req = feedparser.parse(self.session.get(
            "https://mail.google.com/mail/feed/atom/" + label).text)
        num = len(req['entries'])
        update = req['feed']['updated']
        if 'last_update' in self.feed and self.feed['last_update'] == update:
            return
        self.feed['last_update'] = update
        if num == 0:
            return
        if num == 1:
            entry = req['entries'][0]
            msg = entry['title']
            title = entry['author_detail']['name']
            data = entry['link']
        else:
            msg = "{} new messages".format(num)
            data = None
        return (title, msg, "gmail", data, self.handle_notification_callback)
