from flask import Flask, render_template
import back
import json

app = Flask(__name__,static_folder=".",static_url_path='')
texte = {}

@app.route('/new_article', methods=['POST'])
def new_article():
  texte = back.getArticle()
  send = {
    "titre": [],
    "article": []
  }

  i = 0

  for mot in texte["titre"]:
    send["titre"].append({
      "id": i,
      "classes": ["titre", "cache"],
      "mot": "#" * len(mot["mot"]),
      "percentage": 0
    })
    i += 1

  for mot in texte["article"]:
    send["article"].append({
      "id": i,
      "classes": ["article", "cache"],
      "mot": "#" * len(mot["mot"]),
      "percentage": 0
    })
    i += 1
  
  return render_template('index.html', receive=send, receive1 = json.dumps(send))

@app.route('/')
def home():
  return render_template('index.html')


app.run(port=8080, debug=True)