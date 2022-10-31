from flask import Flask, render_template, request
import back
import json

app = Flask(__name__,static_folder=".",static_url_path='')
_back = back.Back()
send = {}

@app.route('/new_article', methods=['POST'])
def new_article():
  texte = _back.getArticle()
  texte1 = _back.testMot("le")
  print(texte1)
  
  return render_template('index.html')#, receive=send, receive1 = json.dumps(send))


# @app.route('/submit', methods=['POST'])
# def submit():

#   return render_template('index.html', receive = send, receive1 = json.dumps(send))

@app.route('/')
def home():
  return render_template('index.html')


app.run(port=8080, debug=True)