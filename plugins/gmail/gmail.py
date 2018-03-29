import feedparser
from google.auth.transport.requests import AuthorizedSession
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


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
                port=8888, open_browser=True, access_type='offline', include_granted_scopes='true')
            self.save_creds()
        else:
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
        return self.feed

    def get_config(self):
        return self.feed

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
        update = req['feed']['updated_parsed']
        if 'last_update' in self.feed and self.feed['last_update'] == update:
            return
        self.feed['last_update'] = update
        if num == 0:
            return
        if num == 1:
            entry = req['entries'][0]
            msg = entry['title']
            title = entry['author_detail']['name']
        else:
            msg = "{} new messages".format(num)
        return (title, msg, "gmail")
