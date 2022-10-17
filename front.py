from flask import Flask, render_template, request
import json

app = Flask(__name__)

if __name__ == '__main__':
    app.run(port=8080, debug=True)


@app.route('/')
def index():
    return render_template('template2.html')
    
@app.route('/tryword')
def tryword():

    if request.method == 'POST':
        if 'reload' in request.form:
            pass # do something

    if request.method == 'GET':
        return render_template('template2.html')

