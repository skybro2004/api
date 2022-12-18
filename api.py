# -*- coding: utf-8 -*- 

isDebug = True

import flask
import urllib.parse as parse
import json, datetime
from flask.templating import render_template

from flask.wrappers import Request
from flask_cors import CORS

from crosswalk import crosswalk


app = flask.Flask(__name__)
app.config['JSON_AS_ASCII'] = False

CORS(app, resources={r'*': {'origins': '*'}})



@app.route("/")
def info():
    pass
    #/templates/index.html로 이동
    return render_template('index.html')



@app.route("/hello")
def hello():
    return "hello"



@app.route("/query")
def query():
    arg = flask.request.args.get("test-query", "default string")
    return "쿼리 : " + arg



@app.route("/crosswalks", methods=['GET', 'POST'])
def manageCrosswalkPos():
    if flask.request.method=='GET':
        dateFrom = flask.request.args.get("dateFrom", datetime.datetime.now().strftime("%Y%m%d"))
        dateTo = flask.request.args.get("dateTo", datetime.datetime.now().strftime("%Y%m%d"))

        return crosswalk.getCrosswalkPos(dateFrom, dateTo)


    if flask.request.method=='POST':
        value = request.form['value']
        date = flask.request.args.get("date", datetime.datetime.now().strftime("%Y%m%d"))

        crosswalk.storeValue(value)
        print(value)
        return value



if __name__=="__main__":
    app.run(host="0.0.0.0", port="5000", threaded=True, debug=isDebug)