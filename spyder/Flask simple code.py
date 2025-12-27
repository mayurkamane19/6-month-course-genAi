from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'good morning mayur'
app.run(host='127.0.0.1')

