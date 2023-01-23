from flask import Flask, render_template, request
import static.python.back as back
import json
import random

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
            print(titreRandom)
            print(titreRandom[:-1])
            texte = _back.getListArticle(titreRandom[:-1])
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

        # On ajoute le titre au fichier texte si il est bon

        if vraiArticle == True and checkIfInList(titreATester) == False:
            with open("./data/articleList.txt", 'a',encoding='utf8') as file:
                file.writelines(titreATester + "\n")

        return {"vraiArticle": vraiArticle}
    else:
        titre = _back.titre
        if not checkIfInList(titre):
            with open("./data/articleList.txt", 'a',encoding='utf8') as file:
                file.writelines(titre + "\n")
        return 'ok'


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
    with open('./data/articleList.txt', 'r', encoding='utf8') as file:
        if titre in file.readlines():
            return True
        else:
            return False


app.run(port=8080, debug=True)