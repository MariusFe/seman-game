from flask import Flask, render_template, request
import static.python.back as back
import json

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

@app.route('/new_article')
def new_article():
    texte = _back.getArticle()
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


app.run(port=8080, debug=True)