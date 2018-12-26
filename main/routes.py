from . import app
from flask import render_template


@app.route('/hello_world')
def route_hello_world():
    return 'Hello World!'


@app.route('/')
def route_index():
    return render_template('index.html')
