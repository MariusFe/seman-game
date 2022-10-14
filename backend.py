from flask import Flask, request

app = Flask(__name__)

@app.route('/message')
def generate_random():
    args = request.args
    print(args['name'])
    return "Hello " + args['name']
    
if __name__ == '__main__':
    app.run()