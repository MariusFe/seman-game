import wikipediaapi
import requests
import re
from gensim.models import KeyedVectors

class Back:

    def __init__(self):
        self.words = {}

    def getArticle(self):
        #Creating the session and preparing the url

        s= requests.Session()
        URL = "https://fr.wikipedia.org/w/api.php"
        taille_article = 1000
        nombre_paragraphes = 10

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

        # If it contains ':' that means it is a discussion, a user or whatever
        # We then loop until we find a article without ':'
        while re.compile(r':').findall(DATA["query"]["random"][0]["title"]):
            R = s.get(url=URL, params=PARAMS)
            DATA = R.json()
            # print(DATA["query"]["random"][0]["title"])
            page_py = wiki_wiki.page(DATA["query"]["random"][0]["title"])
            # print(len(page_py.text.split(" ")))
            # If the article has less than 'taille_article' words we add ':' to the title to loop again
            if len(page_py.text.split(" ")) < taille_article:
                DATA["query"]["random"][0]["title"] = DATA["query"]["random"][0]["title"] + ":"

        # print(page_py.categories)
        # print(page_py.text)
        # print(DATA["query"]["random"][0]["title"])

        # We split in paragraphs (may be useful later) and spaces 
        paragraphes = page_py.text.split("\n")[:nombre_paragraphes]
        paragraphes = [re.split(r" ", par) for par in paragraphes]


        i=0

        self.words = {
            "words":[]
        }

        # TO TEST THE STUFF, REMOVE FOR PRODUCTION
        # titre = "Ceci est un test de titre"
        # paragraphes = [["Ceci","est","un","test","de","texte"]]

        for mot in DATA["query"]["random"][0]["title"].split(" "):
            self.words["words"].append({
                    "mot": mot,
                    "type": "titre",
                    "character": False
            })
            i += 1

        for par in paragraphes:
            for word in par:
                self.words["words"].append({
                    "mot": word,
                    "type": "article",
                    "character": False
                })
                i += 1
            self.words["words"].append({
                "mot": "\n", 
                "type": "article",
                "character": True
            })

        return self.words

    def semantique(self, mot1, mot2):

        try:
            model = KeyedVectors.load_word2vec_format("./data/model.bin", binary=True, unicode_errors="ignore")
            return model.distance(mot1, mot2), model.similarity(mot1, mot2)
        except Exception:
            return None

    def getWords(self):

        return self.words