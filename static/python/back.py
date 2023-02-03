import wikipediaapi
import requests
import re
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
- (not implemented) trigger_exact, if the similarity two words are over this value that means it deserves to be shown as the exact same word ("être" == "est")
- max_similarity_states
- nb_states, the number of possible state for a close word. Can be either, "top", "mitop" or "pastop"
- returned_size, size of the returned json. The number of words that will be displayed on the page (default 500)
- unknown_char, the character used to hide letters in the word, default: "•"

TO DO:
- [X] Split words with characters, example "oui," -> ["oui",","]
- [ ] Work on the trigger
- [ ] Maybe a trigger to say that two words are equal, example: "être" == "est". Trigger at 80% ?
- [ ] Keep only a certain amount of paragraphs
- [ ] Faster loading of the article
"""

class Back:

    def __init__(self):
        self.toIndex = {}
        self.text = {}
        self.taille_article = 1000
        self.nb_paragraphes = 10
        self.trigger_similarity = 0.2
        self.returned_size = 1000
        self.trigger_exact = 0.58
        self.nb_states = 3
        self.max_similarity_states = 0.8
        self.unknownchar = "•"
        self.titre = ""

    def __str__(self):
        string = f"Titre: {self.titre}; taille: {self.taille_article}"
        return string

    def getRandomArticle(self):
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

        toIndex = self.articleToApp(DATA["query"]["random"][0]["title"], page_py.text)

        return toIndex

    def getArticleFromTitre(self, titre):

        wiki_wiki = wikipediaapi.Wikipedia(
            language='fr',
            extract_format=wikipediaapi.ExtractFormat.WIKI
        )

        page_py = wiki_wiki.page(titre)

        toIndex = self.articleToApp(titre, page_py.text)

        return toIndex

    def articleToApp(self, titre, article):

        self.returned_size = 500

        # This dict is for the Back object only, it contains the text in clear and if it is part of the title or not
        self.text = {}
        # This dict is for the index, text blured or found, has way more information than the previous one
        to_index = {}

        # Loop through the title
        # re.split('(\W)', string) splits between words and every other character
        i=0
        for mot in re.split('(\W)',titre):
            self.text[i] = {
                "mot": mot,
                "titre": True
            }
            to_index[i] = {
                "mot": self.unknownchar * len(mot),
                "type": "titre",
                # etat can be 'cache', 'trouve', 'proche', 'new_trouve'
                "etat": ["cache"],
                "percentage": 0
            }
            if(mot.isalpha() == True or mot.isnumeric()): # if the string contains only alpha characters or not (includes accents and weird characters used in the silly french language)
                to_index[i]["character"] = False
            else:
                to_index[i]["mot"] = mot
                to_index[i]["character"] = True
                to_index[i]["etat"] = ["trouve"]
            
            i += 1

        # Loop through the entire article, we keep i to its previous value
        for mot in re.split('(\W)', article):
            self.text[i] = {
                "mot": mot,
                "titre": False
            }
            to_index[i] = {
                "mot": self.unknownchar * len(mot),
                "type": "article",
                "etat": ["cache"],
                "percentage": 0
            }
            
            if(mot.isalpha() == True or mot.isnumeric()):
                to_index[i]["character"] = False
            else:
                to_index[i]["mot"] = mot
                to_index[i]["character"] = True
                to_index[i]["etat"] = ["trouve"]
            i += 1

        # Making sure we will not try to reach a value that does not exist
        if self.returned_size > self.taille_article:
            self.returned_size = self.taille_article


        for i in range(0, self.returned_size):
            self.toIndex[i] = to_index[i]

        self.titre = titre

        print(titre)

        return self.toIndex

    def testMot(self, motToTest, model):

        # We test if the word entered is a real one (COMMENTED because it was not working with proper nouns, it is checked further anyway)
        # try: 
        #     self.model.similarity("bonjour", str(motToTest).lower())
        # except:
        #     return self.toIndex
        
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
                    similarity = model.similarity(str(self.text[i]["mot"]).lower(), str(motToTest).lower())
                except:
                    similarity = 0
                # trigger_smiliraty can be changed based on empirical researchs
                # If the similarity between the actual word and the word entered is larger than the trigger then we can show it to the user
                # We also make sure that the similarity is greater than what it actually is. We won't replace a word if it is "further" from a previous tried word
                if similarity > self.trigger_similarity and similarity > self.toIndex[i]["percentage"]:
                    print(f'Mot entré: {motToTest}, Mot du texte: {self.text[i]["mot"]}, similarité: {similarity}')
                    self.toIndex[i]["percentage"] = float(similarity)
                    step = (self.max_similarity_states-self.trigger_similarity) / self.nb_states
                    
                    if(similarity <= self.trigger_similarity+step):
                        self.toIndex[i]["etat"] = ["pastop"]

                    elif(similarity <= self.trigger_similarity+step*2):
                        self.toIndex[i]["etat"] = ["mitop"]

                    elif(similarity <= self.trigger_similarity+step*3):
                        self.toIndex[i]["etat"] = ["top"]

                    else:
                        self.toIndex[i]["etat"] = ["top"]

                    self.toIndex[i]["etat"].append("proche")



                    # This condition is to check if the tested word is bigger than the actual word or not
                    # Example: 'être' is the actual word
                    # 'avoir' is entered: we return 'avoir' because it has more letters than 'être'
                    # 'es' is entered: we return '#es#' to signify that the actual word is larger than the one entered
                    if len(self.text[i]["mot"]) <= len(motToTest):
                        self.toIndex[i]["mot"] = motToTest
                    elif len(self.text[i]["mot"]) > len(motToTest):
                        self.toIndex[i]["mot"] = math.floor((len(self.text[i]["mot"]) - len(motToTest))/2) * self.unknownchar + motToTest + math.ceil((len(self.text[i]["mot"]) - len(motToTest))/2) * self.unknownchar
            else:
                # It shouldn't enter this, if anything we just return the self.toIndex at the end
                pass

        return self.toIndex

    def tricher(self):
        for i in range(0, len(self.toIndex)):
            if(self.toIndex[i]["character"]) == True:
                pass
            else:
                self.toIndex[i]["etat"] = ["trouve"]
                self.toIndex[i]["mot"] = self.text[i]["mot"]
        return self.toIndex

    def checkTitreArticle(self, titreArticleATester):
        wiki_wiki = wikipediaapi.Wikipedia(
            language='fr',
            extract_format=wikipediaapi.ExtractFormat.WIKI
        )

        page_py = wiki_wiki.page(titreArticleATester)

        # Retourne True si l'article est un vrai
        # Retourne Faux si il est faux
        if (page_py.text == ""):
            return False, ""
        elif (len(page_py.text) < self.returned_size):
            return False, ""
        else:
            return True, page_py.title