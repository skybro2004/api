# -*- coding: utf-8 -*- 

isDebug = False

import flask
import urllib.parse as parse
import json, datetime
from flask.templating import render_template

from flask.wrappers import Request
from flask_cors import CORS

from modules import marker
from modules import schedular
from modules import meal
from modules import survey

app = flask.Flask(__name__)
app.config['JSON_AS_ASCII'] = False

CORS(app, resources={r'*': {'origins': '*'}})



@app.route("/")
def info():
    pass
    #/html/index.html로 이동
    return render_template('index.html')



@app.route("/hello")
def hello():
    return "hello"



@app.route("/query")
def query():
    arg = flask.request.args.get("test-query", "default string")
    return "쿼리 : " + arg



@app.route("/schedular")
def showSchedule():
    officeCode = flask.request.args.get("officeCode", "J10")

    schlCode = flask.request.args.get("schlCode", "7530081")

    grade = flask.request.args.get("grade", "1")

    schlClass = flask.request.args.get("class", "1")

    date = flask.request.args.get("date", datetime.datetime.now().strftime("%Y%m%d"))

    dateRange = flask.request.args.get("range", "day")


    return schedular.getSchedul(officeCode, schlCode, grade, schlClass, date, dateRange)



@app.route("/meal")
def showMeal():
    officeCode = flask.request.args.get("officeCode", "J10")

    schlCode = flask.request.args.get("schlCode", "7530081")

    date = flask.request.args.get("date", datetime.datetime.now().strftime("%Y%m%d"))


    return meal.getMeal(officeCode, schlCode, date)



@app.route("/marker")
def mark():
    studGrade = flask.request.args.get("grade")
    studClass = flask.request.args.get("class")

    bookName = flask.request.args.get("book")
    index = flask.request.args.get("index")
    if bookName==None:
        return json.dumps(marker.getAll(studGrade, studClass))
    else:
        if index==None:
            return json.dumps(marker.getSheet(bookName, 0))
        else:
            return json.dumps(marker.getSheet(bookName, index))
    
    


    """
    데이터 구조
    return json.dumps({
        "code":200,
        header:{
            "bookId":asdf,
            "bookName":adsf,
            grade class .....
        },
        "data":{
            "header":{
                "index":asdf,
                dafasfasfasdf
            },
            "data":{
                1:{"type":"int", "value":5}
                2:{"type":"int", "value":4}
                3:{"type":"int", "value":1}
                4:{"type":"str", "value":"a = 5"}
                5:{"type":"str", "value":"y = 2x^2 + 3x + 5"}
                6:{"type":"img", "value":"https://img.skybro2004.com/asdfsdf"}
            }
        }
    })
    """



@app.route("/image", methods=["GET"])
def getImage():
    category = flask.request.args.get("category", "dccon")
    name = flask.request.args.get("name")
    if name==None:
        return 
    path = f"./images/{category}/"
    return flask.send_file('./modules/images/dccon/asdf.gif',
        mimetype = "image/gif",
        as_attachment=True)
    return flask.send_from_directory(directory="file", filename=path + "asdf.gif")



@app.route("/mealSurvey", methods=["GET"])
def getSurveyData():
    date = flask.request.args.get("date", datetime.datetime.now().strftime("%Y%m%d"))

    res = survey.getSurvey(date)
    if(res==404):
        return json.dumps({"header":{"code":404}})
    else:
        #return {"header":{"code":200, "meal":json.loads(meal.getMeal("J10", "7530081", date))}, "data":res}
        return json.dumps({"header":{"code":200, "meal":json.loads(meal.getMeal("J10", "7530081", date))}, "data":res})
    

@app.route("/mealSurvey", methods=["POST"])
def postSurveyData():
    date = flask.request.args.get("date", datetime.datetime.now().strftime("%Y%m%d"))

    params = json.loads(flask.request.get_data(), encoding='utf-8')
    print(params)
    survey.storeSurvey(date, params)
    return json.dumps({"code":200})



@app.route("/mealMsg", methods=["GET"])
def getMsgData():
    date = flask.request.args.get("date", datetime.datetime.now().strftime("%Y%m%d"))

    res = survey.getMsg(date)
    if(res==404):
        return json.dumps({"header":{"code":404}})
    else:
        pass

    return json.dumps({"header": {"code":200, "date":date}, "data":res})

@app.route("/mealMsg", methods=["POST"])
def postMsgData():
    date = flask.request.args.get("date", datetime.datetime.now().strftime("%Y%m%d"))

    params = json.loads(flask.request.get_data(), encoding='utf-8')
    print(params, type(params))

    survey.storeMsg(date, params["msg"])
    return json.dumps({"code":200})


if __name__=="__main__":
    app.run(host="0.0.0.0", port="5000", threaded=True, debug=isDebug)