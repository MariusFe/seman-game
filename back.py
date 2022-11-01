import wikipediaapi
import requests
import re
from gensim.models import KeyedVectors
import math

class Back:

    def __init__(self, taille_article = 1000, nb_paragraphes = 10, trigger_similarity = 0.2):
        self.toIndex = {}
        self.text = {}
        self.taille_article = taille_article
        self.nb_paragraphes = nb_paragraphes
        self.model = KeyedVectors.load_word2vec_format("./data/model.bin", binary=True, unicode_errors="ignore")
        self.trigger_similarity = trigger_similarity

    def getArticle(self):
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
        page_py = wiki_wiki.page("Bonjour")
        DATA["query"]["random"][0]["title"] = ':'

        # If it contains ':' that means it is a discussion, a user or whatever
        # We then loop until we find a article without ':'
        while re.compile(r':').findall(DATA["query"]["random"][0]["title"]):
            R = s.get(url=URL, params=PARAMS)
            DATA = R.json()
            page_py = wiki_wiki.page(DATA["query"]["random"][0]["title"])
            # If the article has less words than 'taille_article' words we add ':' to the title to loop again
            if len(page_py.text.split(" ")) < self.taille_article:
                DATA["query"]["random"][0]["title"] = DATA["query"]["random"][0]["title"] + ":"

        self.text = {}
        self.toIndex = {}

        i=0
        for mot in DATA["query"]["random"][0]["title"].split(" "):
            self.text[i] = {
                "mot": mot,
                "titre": True
            }
            self.toIndex[i] = {
                "mot": "#" * len(mot),
                "type": "titre",
                "etat": ["cache"],
                "character": False,
                "percentage": 0
            }
            i += 1

        for mot in page_py.text.split(" "):
            self.text[i] = {
                "mot": mot,
                "titre": False
            }
            if mot == "\n":
                self.toIndex[i] = {
                    "mot": "%",
                    "type": "article",
                    "etat": ["cache"],
                    "character": True,
                    "percentage": 0
                }
            else:
                self.toIndex[i] = {
                    "mot": "#" * len(mot),
                    "type": "article",
                    "etat": ["cache"],
                    "character": False,
                    "percentage": 0
                }
            i += 1

        return self.toIndex

    def testMot(self, motToTest):

        try: 
            self.model.similarity("bonjour", motToTest)
        except:
            return self.toIndex

        for i in range(0, len(self.text)):
            if self.toIndex[i]["character"] == True:
                pass
            elif self.text[i]["mot"] == motToTest:
                self.toIndex[i]["mot"] = self.text[i]["mot"]
                self.toIndex[i]["etat"] = ["trouve", "new_trouve"]

            elif "new_trouve" in self.toIndex[i]["etat"]:
                self.toIndex[i]["etat"] = ["trouve"]

            elif "trouve" in self.toIndex[i]["etat"]:
                pass 

            elif "trouve" not in self.toIndex[i]["etat"]:
                try:
                    similarity = self.model.similarity(self.text[i]["mot"], motToTest)
                except:
                    similarity = 0
                if similarity > self.trigger_similarity and similarity > self.toIndex[i]["percentage"]:
                    self.toIndex[i]["percentage"] = similarity
                    self.toIndex[i]["etat"] = ["proche"]

                    if len(self.text[i]["mot"]) <= len(motToTest):
                        self.toIndex[i]["mot"] = motToTest
                    elif len(self.text[i]["mot"]) > len(motToTest):
                        self.toIndex[i]["mot"] = math.floor((len(self.text[i]["mot"]) - len(motToTest))/2) * "#" + motToTest + math.ceil((len(self.text[i]["mot"]) - len(motToTest))/2) * "#"


        return self.toIndex