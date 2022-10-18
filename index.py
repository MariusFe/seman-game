from flask import Flask, render_template
import back

app = Flask(__name__,static_folder=".",static_url_path='')
texte = {}

@app.route('/new_article', methods=['POST'])
def new_article():
  texte = back.getArticle()
  send = {
    "titre": [],
    "mots": []
  }

  i = 0

  for mot in texte["titre"]:
    send["titre"].append({
      "id": i,
      "classes": ["titre", "cache"],
      "mot": " " * len(mot["mot"]),
      "percentage": 0
    })
    i += 1
  
  return render_template('index.html', receive=send)

@app.route('/')
def home():
  return render_template('index.html')


app.run(port=8080, debug=True)