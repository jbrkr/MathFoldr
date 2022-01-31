#!/usr/bin/python3

import requests

S = requests.Session()

URL = "https://en.wikipedia.org/w/api.php"
def get_subcats(cat):
    PARAMS = {
        "action": "query",
        "cmtitle": cat,
        "cmtype": "subcat",
        "list": "categorymembers",
        "format": "json"
    }

    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()

    PAGES = DATA["query"]["categorymembers"]

    return [page["title"] for page in PAGES]
