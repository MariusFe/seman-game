import wikipediaapi
import requests
import re


def getArticle():
    #Creating the session and preparing the url
    s= requests.Session()
    URL = "https://fr.wikipedia.org/w/api.php"

    PARAMS = {
        "action": "query",
        "format": "json",
        "list": "random"
    }

    wiki_wiki = wikipediaapi.Wikipedia(
        language='fr',
        extract_format=wikipediaapi.ExtractFormat.WIKI
    )

    # We are getting a random article
    R = s.get(url=URL, params=PARAMS)
    DATA = R.json()
    DATA["query"]["random"][0]["title"] = ':'

    # If it contains ':' that means it is a discussion, a user 
    while re.compile(r':').findall(DATA["query"]["random"][0]["title"]):
        R = s.get(url=URL, params=PARAMS)
        DATA = R.json()
        # print(DATA["query"]["random"][0]["title"])
        page_py = wiki_wiki.page(DATA["query"]["random"][0]["title"])
        # print(len(page_py.text.split(" ")))
        if len(page_py.text.split(" ")) < 1000:
            DATA["query"]["random"][0]["title"] = DATA["query"]["random"][0]["title"] + ":"

    # print(page_py.categories)
    # print(page_py.text)
    # print(DATA["query"]["random"][0]["title"])
    return page_py.text, DATA["query"]["random"][0]["title"]