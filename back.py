import wikipediaapi
import requests
import re
from gensim.models import KeyedVectors
import math

"""
Back object

- Instantiate the article
- Contains the article in clear
- Returns the blured article to the index to be displayed with all the "states" of the words
- Try a word entered by the user


Takes:
- taille_article, number of words per article we want. We skip the small articles
- nb_paragraphes, number of paragraphes we take in the article chosen. We avoid to display too much text
- trigger_similarity, if two words are less than (default, to be adjusted) 20% similar we don't show it to the user
- returned_size, size of the returned json. The number of words that will be displayed on the page (default 100)
- (not implemented) trigger_exact, if the similarity two words are over this value that means it deserves to be shown as the exact same word ("être" == "est")

TO DO:
- Split words with characters, example "oui," -> ["oui",","]
- Work on the trigger
- Maybe a trigger to say that two words are equal, example: "être" == "est". Trigger at 80% ?
"""

class Back:

    def __init__(self, taille_article = 1000, nb_paragraphes = 10, trigger_similarity = 0.2, returned_size = 100, trigger_exact = 0.58):
        self.toIndex = {}
        self.text = {}
        self.taille_article = taille_article
        self.nb_paragraphes = nb_paragraphes
        self.model = KeyedVectors.load_word2vec_format("./data/model.bin", binary=True, unicode_errors="ignore")
        self.trigger_similarity = trigger_similarity
        self.returned_size = returned_size
        self.trigger_exact = trigger_exact

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

        # This dict is for the Back object only, it contains the text in clear and if it is part of the title or not
        self.text = {}
        # This dict is for the index, text blured or found, has way more information than the previous one
        to_index = {}

        # Loop through the title
        # re.split('(\W)', string) splits between words and every other character
        i=0
        for mot in re.split('(\W)',DATA["query"]["random"][0]["title"]):
            self.text[i] = {
                "mot": mot,
                "titre": True
            }
            to_index[i] = {
                "mot": "#" * len(mot),
                "type": "titre",
                # etat can be 'cache', 'trouve', 'proche', 'new_trouve'
                "etat": ["cache"],
                "percentage": 0
            }
            if(mot.isalpha() == True): # if the string contains only alpha characters or not (includes accents and weird characters used in the silly french language)
                to_index[i]["character"] = False
            else:
                to_index[i]["mot"] = mot
                to_index[i]["character"] = True
            
            i += 1

        # Loop through the entire article, we keep i to its preivous value
        for mot in re.split('(\W)', page_py.text):
            self.text[i] = {
                "mot": mot,
                "titre": False
            }
            to_index[i] = {
                "mot": "#" * len(mot),
                "type": "article",
                "etat": ["cache"],
                "percentage": 0
            }
            
            if(mot.isalpha() == True):
                to_index[i]["character"] = False
            else:
                to_index[i]["mot"] = mot
                to_index[i]["character"] = True
            i += 1

        for i in range(0, self.returned_size):
            self.toIndex[i] = to_index[i]

        print(DATA["query"]["random"][0]["title"])

        return self.toIndex

    def testMot(self, motToTest):

        # We test if the word entered is a real one
        try: 
            self.model.similarity("bonjour", str(motToTest).lower())
        except:
            return self.toIndex
        
        for i in range(0, len(self.toIndex)):
            # If it is a character we pass, it shouldn't enter here, redundancy with the previous try
            if self.toIndex[i]["character"] == True:
                pass
            # If it is exactly the word we looked for we replace the word by 
            elif str(self.text[i]["mot"]).lower() == str(motToTest).lower():
                self.toIndex[i]["mot"] = self.text[i]["mot"]
                self.toIndex[i]["etat"] = ["trouve", "new_trouve"]

            # If the word has been found previously then we remove the new_trouve (changing back the background color to gray)
            elif "new_trouve" in self.toIndex[i]["etat"]:
                self.toIndex[i]["etat"] = ["trouve"]

            elif "trouve" in self.toIndex[i]["etat"]:
                pass 

            # We will check for the similarity if the word is not found already
            elif "trouve" not in self.toIndex[i]["etat"]:
                # We try once again to be sure, redundancy, the last thing we want is the server to crash
                try:
                    similarity = self.model.similarity(str(self.text[i]["mot"]).lower(), str(motToTest).lower())
                except:
                    similarity = 0
                # trigger_smiliraty can be changed based on empirical researchs
                # If the similarity between the actual word and the word entered is larger than the trigger then we can show it to the user
                # We also make sure that the similarity is greater than what it actually is. We won't replace a word if it is "further" from a previous tried word
                if similarity > self.trigger_similarity and similarity > self.toIndex[i]["percentage"]:
                    print(f'Mot entré: {motToTest}, Mot du texte: {self.text[i]["mot"]}, similarité: {similarity}')
                    self.toIndex[i]["percentage"] = float(similarity)
                    self.toIndex[i]["etat"] = ["proche"]

                    # This condition is to check if the tested word is bigger than the actual word or not
                    # Example: 'être' is the actual word
                    # 'avoir' is entered: we return 'avoir' because it has more letters than 'être'
                    # 'es' is entered: we return '#es#' to signify that the actual word is larger than the one entered
                    if len(self.text[i]["mot"]) <= len(motToTest):
                        self.toIndex[i]["mot"] = motToTest
                    elif len(self.text[i]["mot"]) > len(motToTest):
                        self.toIndex[i]["mot"] = math.floor((len(self.text[i]["mot"]) - len(motToTest))/2) * "#" + motToTest + math.ceil((len(self.text[i]["mot"]) - len(motToTest))/2) * "#"
            else:
                # It shouldn't enter this, if anything we just return the self.toIndex at the end
                pass

        return self.toIndex