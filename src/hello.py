from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    #return 'This is sample application running on Flask! ADDING KUBERNETES'
    return render_template('index.html')
