from flask import Flask, render_template, request
import back
import json

app = Flask(__name__,static_folder=".",static_url_path='')
_back = back.Back()
send = {}

@app.route('/new_article', methods=['POST'])
def new_article():
  texte = _back.getArticle()
  for i in range(0, len(texte)):
    send[i] = {
      "mot": texte[i]["mot"],
      "classes": texte[i]["etat"],
      "percentage": texte[i]["mot"]
    }
    send[i]["classes"].append(texte[i]["type"])
  
  return render_template('index.html', receive=send, receive1 = json.dumps(send))


@app.route('/submit', methods=['POST'])
def submit():
  print(request.form.get("in_word"))
  texte = _back.testMot(request.form.get("in_word"))
  send = {}
  for i in range(0, len(texte)):
    send[i] = {
      "mot": texte[i]["mot"],
      "classes": texte[i]["etat"],
      "percentage": texte[i]["percentage"]
    }
    send[i]["classes"].append(texte[i]["type"])

  print(send)
    
  return render_template('index.html', receive = send, receive1 = json.dumps(send))

@app.route('/')
def home():
  return render_template('index.html')


app.run(port=8080, debug=True)