import wikipediaapi
import requests
import re
from gensim.models import KeyedVectors


def getArticle():
    #Creating the session and preparing the url

    s= requests.Session()
    URL = "https://fr.wikipedia.org/w/api.php"
    taille_article = 1000
    nombre_paragraphes = 1

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
        if len(page_py.text.split(" ")) < taille_article:
            DATA["query"]["random"][0]["title"] = DATA["query"]["random"][0]["title"] + ":"

    # print(page_py.categories)
    # print(page_py.text)
    # print(DATA["query"]["random"][0]["title"])

    paragraphes = page_py.text.split("\n")[:nombre_paragraphes]
    paragraphes = [re.split(r" ", par) for par in paragraphes]
    return page_py.text, DATA["query"]["random"][0]["title"], paragraphes

def semantique(mot1, mot2):

  model = KeyedVectors.load_word2vec_format("./data/model.bin", binary=True, unicode_errors="ignore")
  return model.distance(mot1, mot2), model.similarity(mot1, mot2)