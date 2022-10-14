from flask import Flask, render_template 
from flaskext.markdown import Markdown
import json
from pygments.formatters import HtmlFormatter

app = Flask(__name__)
Markdown(app)

article = open("article.txt","r",encoding='utf-8').read()

articlesplit = article.split(" ")

dictionary = {"mot":[],"id":[],"nmlettre":[],"trouve":[],"motproche":[]};

i=0
for word in articlesplit:
    dictionary["mot"].append(word)
    dictionary["id"].append(i)
    dictionary["nmlettre"].append(len(word))
    dictionary["trouve"].append(0)
    dictionary["motproche"].append("")
    i=i+1

mots = ""
for word in dictionary["mot"]:
    mots = mots + '<div>' + word + '</div>'

@app.route('/')
def echo():
    return render_template('template.html',article=article,mots=mots,mkd_text="!>spoiler")
    
if __name__ == '__main__':
    app.run(port=8080, debug=True)