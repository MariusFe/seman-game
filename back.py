import wikipediaapi
import requests
import re
from gensim.models import KeyedVectors

class Back:

    def __init__(self, taille_article = 1000, nb_paragraphes = 10):
        self.toIndex = {}
        self.text = {}
        self.taille_article = taille_article
        self.nb_paragraphes = nb_paragraphes
        self.model = KeyedVectors.load_word2vec_format("./data/model.bin", binary=True, unicode_errors="ignore")

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
        DATA["query"]["random"][0]["title"] = ':'

        # If it contains ':' that means it is a discussion, a user or whatever
        # We then loop until we find a article without ':'
        while re.compile(r':').findall(DATA["query"]["random"][0]["title"]):
            R = s.get(url=URL, params=PARAMS)
            DATA = R.json()
            # print(DATA["query"]["random"][0]["title"])
            page_py = wiki_wiki.page(DATA["query"]["random"][0]["title"])
            # print(len(page_py.text.split(" ")))
            # If the article has less words than 'taille_article' words we add ':' to the title to loop again
            if len(page_py.text.split(" ")) < self.taille_article:
                DATA["query"]["random"][0]["title"] = DATA["query"]["random"][0]["title"] + ":"

        # We split in paragraphs (may be useful later) and spaces 
        # paragraphes = page_py.text.split("\n")[:self.nombre_paragraphes]
        # paragraphes = [re.split(r" ", par) for par in paragraphes]





        self.text = {}
        self.toIndex = {}
        self.taille_titre = len(DATA["query"]["random"][0]["title"].split(" "))

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
                "character": False
            }
            i += 1

        for mot in page_py.text.split(" "):
            self.text[i] = {
                "mot": mot,
                "titre": False
            }
            if mot == "\n":
                self.toIndex[i] = {
                    "mot": "#" * len(mot),
                    "type": "article",
                    "etat": ["cache"],
                    "character": False
                }
            else:
                self.toIndex[i] = {
                        "mot": "#" * len(mot),
                        "type": "article",
                        "etat": ["cache"],
                        "character": False
                    }
            i += 1

        return self.toIndex

    def testMot(self, motToTest):

        try: 
            model.similarity("bonjour", motToTest)
        except:
            print("Le mot n'existe pas")

        i = 0
        for mot in self.text:
            if mot == motToTest:
                self.toIndex[i]["mot"] = mot
                self.toIndex[i]["classe"] = ["trouve", "new_trouve"]

            elif "new_trouve" in self.toIndex[i]["classe"]:
                self.toIndex[i]["classe"] = ["trouve"]

            elif "trouve" in self.toIndex[i]["classe"]:
                pass 

            elif "trouve" not in self.toIndex[i]["classe"]:
                similarity = model.similarity(mot["mot"], motToTest)
                if similarity > 0.2 and similarity > self.toIndex[i]["percentage"]:
                    self.toIndex[i]["percentage"] = similarity
                    self.toIndex[i]["classe"] = ["proche"]

                    if len(mot) <= len(motToTest):
                        self.toIndex[i]["mot"] = motToTest
                    elif len(mot) > len(motToTest):
                        self.toIndex[i]["mot"] = math.floor((len(mot) - len(motToTest))/2) * "#" + motToTest + math.ceil((len(mot) - len(motToTest))/2) * "#"


        return toIndex
