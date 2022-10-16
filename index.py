from flask import Flask, render_template
import back

app = Flask(__name__,static_folder=".",static_url_path='')
texte ={}

@app.route('/')
def home():
  texte = back.getArticle()
  return render_template('index.html', titre=texte["titre"])

app.run(port=8080, debug=True)

# oui