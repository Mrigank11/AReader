# AReader
It is a python-based project which notifies you of updates from various feeds like `Gmail`, `Atom/RSS` etc.
- Plugin based structure, so its easy to add new sources.
- **Gmail** and **Atom** readers included
## Installation
- Clone repo
```
git clone https://github.com/Mrigank11/AReader
```
- Install dependencies: `pip install -r requirements.txt`
- Run : `python main.py`
### Add Atom/RSS Source:
Add an object to areader.json:
```json
{
    "provider":"rss",
    "url":"<url to atom/rss feed>",
    "title":"<notification title>(Optional)"
}
```
### Add Gmail Source:
- Create a project on console.developers.google.com
- Create new WebApp and download credentials
- Paste it in `plugins/gmail/client_server.json`
- Add an object to areader.json:
```json
{
    "provider":"gmail",
    "alias":"<identifier of gmail id>(Optional)",
    "label":"<label to fetch>(Optional)"
}
```
- At first run, your browser will open for authorizing each entry having `gmail` as `provider` in the order of appearance in `areader.json`