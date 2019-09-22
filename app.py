from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, We are in the right way!'

if __name__ == '__main__':
    app.run()