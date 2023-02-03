from flask import Flask, render_template, request, session
import static.python.back as back
import json
import random
import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from gensim.models import KeyedVectors
from flask_session import Session

"""
Index Flask

TO DO
- Session for users, currently the same article is used for every users
- Shared session
- Overall statistics, working with a database ? or simply or global json
- More ?
"""
# Load .env and keys
load_dotenv()
KEY = os.getenv('KEY')
APP_KEY = os.getenv('APP_KEY')

# Create the app, session and the model
app = Flask(__name__,template_folder= "./static/html")
app.secret_key = APP_KEY
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
model = KeyedVectors.load_word2vec_format("./data/model.bin", binary=True, unicode_errors="ignore")


# Create a new article
@app.route('/new_article', methods=['POST'])
def new_article():
    _back = back.Back()
    _back.__dict__.update(session['back'])

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
    session.clear()
    session['back'] = _back.__dict__
    return json.dumps(send)

# Submit a word
@app.route('/submit', methods=['POST'])
def submit():
    _back = back.Back()
    _back.__dict__.update(session['back'])
    print(request.get_json()['in_word'])
    texte = _back.testMot(request.get_json()['in_word'], model)
    send = fromBacktoIndex(texte)
    
    session['back'] = _back.__dict__
    return json.dumps(send)

# Root
@app.route('/')
def home():
    session['back'] = back.Back().__dict__
    return render_template('index.html')

# If the user wants to cheat
@app.route('/tricher')
def tricher():
    
    _back = back.Back()
    _back.__dict__.update(session['back'])
    
    texte = _back.tricher()
    send  = fromBacktoIndex(texte)

    session['back'] = _back.__dict__
    return json.dumps(send)

# When the user wants to add article to the list
@app.route('/selectArticle')
def selectArticle():
    return render_template('selectArticle.html')
 
# Article being added to the list
@app.route('/add_article', methods=['POST', 'GET'])
def addArticle():
    _back = back.Back()
    _back.__dict__.update(session['back'])

    if request.method == 'POST':
        # Tester si le mot est vrai ou pas
        # return True: le texte entré est un vrai article
        # return False: le texte entré n'est pas un vrai article
        titreATester = request.get_json()['article']
        vraiArticleBool, vraiArticleNom = _back.checkTitreArticle(titreATester)
        inList = checkIfInList(titreATester)

        # On ajoute le titre au fichier texte si il est bon

        if vraiArticleBool == True and  inList == False:
            with open("./data/articleList.txt", 'a',encoding='utf8') as file:
                file.writelines(vraiArticleNom + "\n")

        session['back'] = _back.__dict__
        return {
            "vraiArticle": vraiArticleBool,
            "inList": inList
        }

    # Si méthode GET on ajoute le titre de l'article actuel, on est sûr qu'il est bon
    else:
        titre = _back.titre
        if not checkIfInList(titre):
            with open("./data/articleList.txt", 'a',encoding='utf8') as file:
                file.writelines(titre + "\n")

        session['back'] = _back.__dict__
        return 'ok'

# Routes to get or post the code of an article
@app.route('/code_article', methods=['POST', 'GET'])
def genererCodeArticle():
    _back = back.Back()
    _back.__dict__.update(session['back'])

    # Si méthode GET on renvoie le code crypté à l'utilisateur
    if request.method == 'GET':
        try:
            titreCrypte = Fernet(KEY).encrypt(_back.titre.encode()).decode()
            send = {'titre_crypte': titreCrypte}
            session['back'] = _back.__dict__
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
                session['back'] = _back.__dict__
                return json.dumps(send)
        except:
            return "Error"

# Route to get an article with a code in the url
# WIP
@app.route('/article', methods=['POST'])
def articleURL():

    code = request.args.get('code')

    return render_template('index.html')

# This function takes a dict returned from the back to transform it to a json read by the JavaScript in the .html doc
# We could just directly return the correct format from the Back object I know but that means I need to redo a lot (flemme + ratio)
# The format is 
# {
#     "0": {
#         "id" : 0,
#         "mot": mot,
#         "classes": ["article","trouve"], # or "top", "mitop", "pastop", "cache", "titre", "character", "new_trouve"
#         "percentage": 1, # between 0 and 1
#         "character": False
#     },
#     "1" :{
#     ...
#     }
# }

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


# Deletion of the session files before starting the server
# So the server is not building up data over time even after a restart
# May be useful if we want to track user stats, we will see for later
try:
    folder = './flask_session/'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        os.remove(file_path)
except:
    pass

app.run(port=8087, host='0.0.0.0', debug=True)