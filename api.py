# -*- coding: utf-8 -*- 

isDebug = False

import flask
import urllib.request as ul
import urllib.parse as parse
import json, datetime, re
from flask.templating import render_template

from flask.wrappers import Request
from flask_cors import CORS

import marker
from marker import getAll, getSheet

app = flask.Flask(__name__)
app.config['JSON_AS_ASCII'] = False

CORS(app, resources={r'*': {'origins': '*'}})
neisKey = "028278aaacd242438668d46a5464e934"

def selectSubject(grade, schlClass, sub):
    if grade=="2":
        if schlClass=="3":
            if "화학" in sub:
                return "선택 A"
            elif "중국어" in sub:
                return "선택 C"
            elif "정치" in sub:
                return "선택 D"
            elif "심화 영어 독해" in sub:
                return "선택 E"
            elif "생명" in sub:
                return "선택 F"

        elif schlClass=="8":
            if "고전문학" in sub:
                return "선택 A"
            elif "생활과" in sub:
                return "선택 C"
            elif "생명" in sub:
                return "선택 D"
            elif "지구과학" in sub:
                return "선택 E"
            elif "기하" in sub:
                return "선택 F"

        elif schlClass=="9":
            if "생명" in sub:
                return "선택 A"
            elif "지구" in sub:
                return "선택 D"

    return sub


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
    arg = flask.request.args.get("test-query")
    return "쿼리 : " + arg

@app.route("/schedular")
def returnSchedule():
    date = flask.request.args.get("date")
    if date==None:
        date = datetime.datetime.now().strftime("%Y%m%d")
    grade = flask.request.args.get("grade")
    if grade==None:
        grade = 1
    schlClass = flask.request.args.get("class")
    if schlClass==None:
        schlClass = 1
    year = int(date[0:4])
    month = int(date[4:6])
    day = int(date[6:8])
    weekday = datetime.date(year, month, day).weekday()
    dateFrom = datetime.datetime(year, month, day)
    dateTo = datetime.datetime(year, month, day)
    dateFrom -= datetime.timedelta(days=weekday)
    dateTo += datetime.timedelta(days=(4-weekday))
    if 4<weekday:
        dateFrom += datetime.timedelta(days=7)
        dateTo += datetime.timedelta(days=7)
    dateFrom = dateFrom.strftime("%Y%m%d")
    dateTo = dateTo.strftime("%Y%m%d")

    url = f"https://open.neis.go.kr/hub/hisTimetable?KEY={neisKey}&Type=json"
    url += f"&Type=json"
    url += f"&ATPT_OFCDC_SC_CODE=J10"
    url += f"&SD_SCHUL_CODE=7530081"
    url += f"&GRADE={grade}"
    url += f"&CLASS_NM={schlClass}"
    url += f"&TI_FROM_YMD={dateFrom}&TI_TO_YMD={dateTo}"

    request = ul.Request(url)
    response = ul.urlopen(request)
    if response.getcode()==200:
        responseData = response.read()
        responseData = json.loads(responseData)
        try:
            if responseData["RESULT"]["MESSAGE"]=="해당하는 데이터가 없습니다.":
                print("code : 404")
                return json.dumps({"code":404})
        except KeyError:
            pass
        #print(responseData)
        responseData = responseData["hisTimetable"][1]["row"]
        result = []
        weekday_arr = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
        for item in responseData:
            date = item["ALL_TI_YMD"]
            weekday = datetime.date(int(date[0:4]), int(date[4:6]), int(date[6:8])).weekday()
            result.append({"weekday":weekday, "weekday_str":weekday_arr[weekday], "period":item["PERIO"], "item":selectSubject(grade, schlClass, item["ITRT_CNTNT"])})
        return json.dumps({"code":200, "header":{"dateFrom":dateFrom, "dateTo":dateTo}, "data":result})
    else:
        print(f"code : {response.getcode()}")
        return json.dumps({"code":response.getcode()})

@app.route("/meal")
def meal():
    date = flask.request.args.get("date")
    if date==None:
        date = datetime.datetime.now().strftime("%Y%m%d")
    year = int(date[0:4])
    month = int(date[4:6])
    day = int(date[6:8])
    url = f"https://open.neis.go.kr/hub/mealServiceDietInfo?KEY={neisKey}&Type=json"
    url += f"&ATPT_OFCDC_SC_CODE=J10&SD_SCHUL_CODE=7530081"
    url += f"&MLSV_FROM_YMD={date}&MLSV_TO_YMD={date}"

    request = ul.Request(url)
    response = ul.urlopen(request)
    if response.getcode()==200:
        responseData = response.read()
        responseData = json.loads(responseData)
        try:
            responseData = responseData["mealServiceDietInfo"][1]["row"][0]
        except KeyError:
            return json.dumps({"code":404, "meal":"급식이 없어요!"})
        meals_raw = responseData["DDISH_NM"]
        meals_raw = list(meals_raw.split("<br/>"))
        meals = []
        for meal in meals_raw:
            meal = meal.split("(7)")[0]
            meal = re.sub('[0-9]*\.', '', meal)
            meals.append(meal)
        Calorie = responseData["CAL_INFO"]
        print(meals)
        return json.dumps({"code":200, "meal":meals, "cal":Calorie})

    else:
        return json.dumps({"code":response.getcode()})


@app.route("/marker")
def marker():
    studGrade = flask.request.args.get("grade")
    studClass = flask.request.args.get("class")

    bookName = flask.request.args.get("book")
    index = flask.request.args.get("index")
    if bookName==None:
        return json.dumps(getAll(studGrade, studClass))
    else:
        if index==None:
            return json.dumps(getSheet(bookName, 0))
        else:
            return json.dumps(getSheet(bookName, index))
    
    


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

if __name__=="__main__":
    app.run(host="0.0.0.0", port="5000", debug=isDebug)