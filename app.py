from flask import Flask, render_template, request, session
import static.python.back as back
import json
import random
import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

"""
Index Flask

TO DO
- Session for users, currently the same article is used for every users
- Shared session
- Overall statistics, working with a database ? or simply or global json
- More ?
"""

app = Flask(__name__,template_folder= "./static/html")
_back = back.Back(returned_size=300)

load_dotenv()
KEY = os.getenv('KEY')

@app.route('/new_article', methods=['POST'])
def new_article():

    # Si l'utilisateur a sélectionné un article aléatoire parmi tout wikipedia
    if request.get_json()['random'] == True:
        texte = _back.getRandomArticle()
        send = fromBacktoIndex(texte)
    
    # Si l'utilisateur a selectionné un article aléatoire parmi la liste
    else:
        with open('./data/articleList.txt', 'r', encoding='utf') as file:
            data = file.readlines()
            titreRandom = random.choice(data)
            texte = _back.getArticleFromTitre(titreRandom[:-1])
            send = fromBacktoIndex(texte)
  
    return json.dumps(send)


@app.route('/submit', methods=['POST'])
def submit():
    print(request.get_json()['in_word'])
    texte = _back.testMot(request.get_json()['in_word'])
    send = fromBacktoIndex(texte)
    
    return json.dumps(send)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/tricher')
def tricher():
    texte = _back.tricher()
    send  = fromBacktoIndex(texte)
    return json.dumps(send)

@app.route('/selectArticle')
def selectArticle():
    return render_template('selectArticle.html')

@app.route('/add_article', methods=['POST', 'GET'])
def addArticle():
    if request.method == 'POST':
        # Tester si le mot est vrai ou pas
        # return True: le texte entré est un vrai article
        # return False: le texte entré n'est pas un vrai article
        titreATester = request.get_json()['article']
        vraiArticle = _back.checkTitreArticle(titreATester)
        inList = checkIfInList(titreATester)

        # On ajoute le titre au fichier texte si il est bon

        if vraiArticle == True and  inList == False:
            with open("./data/articleList.txt", 'a',encoding='utf8') as file:
                file.writelines(titreATester + "\n")

        return {
            "vraiArticle": vraiArticle,
            "inList": inList
        }

    # Si méthode GET on ajoute le titre de l'article actuel, on est sûr qu'il est bon
    else:
        titre = _back.titre
        if not checkIfInList(titre):
            with open("./data/articleList.txt", 'a',encoding='utf8') as file:
                file.writelines(titre + "\n")
        return 'ok'

@app.route('/code_article', methods=['POST', 'GET'])
def genererCodeArticle():

    # Si méthode GET on renvoie le code crypté à l'utilisateur
    if request.method == 'GET':
        try:
            titreCrypte = Fernet(KEY).encrypt(_back.titre.encode()).decode()
            send = {'titre_crypte': titreCrypte}
            return json.dumps(send)
        except:
            return "Error"

    # Si méthode POST on vérifie que le code entrer est bon
    # On renvoie un json pour le front si ok
    # Sinon on renvoie une erreur pour l'utilisateur
    else:
        code = request.get_json()['code']
        try: # Si le code c'est du n'importe quoi le truc peut planter du coup on retourne juste rien si jamais
            titre = Fernet(KEY).decrypt(code.encode()).decode()
            if(_back.checkTitreArticle(titre) == False):
                return "Error"
            else:
                texte = _back.getArticleFromTitre(titre)
                send = fromBacktoIndex(texte)
                return json.dumps(send)
        except:
            return "Error"

@app.route('/article', methods=['POST'])
def articleURL():

    code = request.args.get('code')

    return render_template('index.html')






# This function takes a dict returned from the back to transform it to a json read by the JavaScript in the .html doc
# We could just directly return the correct format from the Back object I know but that means I need to redo a lot (flemme + ratio)

def fromBacktoIndex(texte):
    send = {}
    for i in range(0, len(texte)):
        send[i] = {
            "id": i,
            "mot": texte[i]["mot"],
            "classes": texte[i]["etat"],
            "percentage": texte[i]["percentage"]
        }
        send[i]["classes"].append(texte[i]["type"])
        if texte[i]["character"] == True:
            send[i]["classes"].append("character")
    return send

# Check if the input title is in the list of all the articles, do not put twice the same article
def checkIfInList(titre):

    file = open('./data/articleList.txt', 'r', encoding='utf8')
    for titreListe in file.readlines():
        if titre.lower() == titreListe[:-1].lower():
            return True

    return False


app.run(port=8080, debug=True)