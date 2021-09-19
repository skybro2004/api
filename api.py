import flask
import urllib.request as ul
import urllib.parse as parse
import json, datetime

app = flask.Flask(__name__)

neisKey = "028278aaacd242438668d46a5464e934"

@app.route("/")
def hello():
    return "hello"

@app.route("/schedular/<date>")
def returnSchedule(date):
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

    url =  f"https://open.neis.go.kr/hub/hisTimetable?KEY={neisKey}&Type=json"
    url += f"&Type=json"
    url += f"&ATPT_OFCDC_SC_CODE=J10"
    url += f"&SD_SCHUL_CODE=7530081"
    url += f"&GRADE=2"
    url += f"&CLASS_NM=8"
    url += f"&TI_FROM_YMD={dateFrom}&TI_TO_YMD={dateTo}"

    request = ul.Request(url)
    response = ul.urlopen(request)
    if response.getcode()==200:
        responseData = response.read()
        responseData = json.loads(responseData)
        try:
            if responseData["RESULT"]["MESSAGE"]=="해당하는 데이터가 없습니다.":
                return {"code":404}
        except KeyError:
            pass

        responseData = responseData["hisTimetable"][1]["row"]
        result = []
        for item in responseData:
            print(item["ALL_TI_YMD"], item["PERIO"], item["ITRT_CNTNT"])
            result.append({"weekday":weekday, "period":item["PERIO"], "item":item["ITRT_CNTNT"]})
        return {"code":200, "data":result}
    else:
        return {"code":response.getcode()}


if __name__=="__main__":
    app.run()