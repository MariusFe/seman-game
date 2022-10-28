from flask import Flask, render_template, request
import back
import json

app = Flask(__name__,static_folder=".",static_url_path='')
_back = back.Back()
send = {}

@app.route('/new_article', methods=['POST'])
def new_article():
  texte = _back.getArticle()
  send = {
    "words": []
  }

  i = 0

  for mot in texte["words"]:
    send["words"].append({
        "id": i,
        "mot": "#" * len(mot["mot"]),
        "type": mot["type"],
        "etat": ["cache"],
        "percentage": 0,
        "character": mot["character"]
      })
    i += 1
  
  return render_template('index.html', receive=send, receive1 = json.dumps(send))


@app.route('/submit', methods=['POST'])
def submit():

  submit = request.form.get("in_word")
  result = _back.semantique("oui", submit)
  words = _back.getWords()

  if result == None:
    return render_template('index.html', receive = send, receive1 = json.dumps(send))

  i = 0
  for word in words:

    if submit == word:
      send["words"][i]["mot"] = word
      send["words"][i]["classes"] = [part, "trouve"]

    if result[1] > 0.2 and submit != word:
      send["words"][i]["mot"] = submit
      send["words"][i]["classes"] = [part, "proche"]
      send["words"][i]["percentage"] = result[1]

    i += 1

  return render_template('index.html', receive = send, receive1 = json.dumps(send))

@app.route('/')
def home():
  return render_template('index.html')


app.run(port=8080, debug=True)