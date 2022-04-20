from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello():
    #return 'This is sample application running on Flask! ADDING KUBERNETES'
    return render_template('index.html')
