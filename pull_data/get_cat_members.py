#!/usr/bin/python3

import requests

S = requests.Session()

URL = "https://en.wikipedia.org/w/api.php"
def get_cat_members(cat):
        PARAMS = {
            "action": "query",
            "cmtitle": f"Category:{cat}",
            "cmlimit": "500",
            "list": "categorymembers",
            "format": "json"
        }

        R = S.get(url=URL, params=PARAMS)
        DATA = R.json()

        PAGES = DATA['query']['categorymembers']

        return [page['title'] for page in PAGES]
