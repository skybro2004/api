import urllib.request as ul
import ssl
import datetime, json

neisKey = "028278aaacd242438668d46a5464e934"
path = "/home/sj/api"


subjectData = {}
with open(f"{path}/modules/schedular.json", "r") as raw_data:
    subjectData = json.load(raw_data)

def selectSubject(grade, schlClass, sub):
    """if grade=="2":

        if schlClass=="1":
            if "경제" in sub:
                return "선택 A"
            elif "세계사" in sub:
                return "선택 C"
            elif "윤리" in sub:
                return "선택 D"
            elif "생명" in sub:
                return "선택 E"
            elif "일본어" in sub:
                return "선택 F"

        elif schlClass=="2":
            if "일본어" in sub:
                return "선택 A"
            elif "고전문학" in sub:
                return "선택 C"
            elif "정보" in sub:
                return "선택 D"
            elif "윤리" in sub:
                return "선택 E"
            elif "세계지리" in sub:
                return "선택 F"

        elif schlClass=="3":
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

        elif schlClass=="4":
            if "정치" in sub:
                return "선택 A"
            elif "생명" in sub:
                return "선택 C"
            elif "생활과" in sub:
                return "선택 D"
            elif "화학" in sub:
                return "선택 E"
            elif "중국어" in sub:
                return "선택 F"

        elif schlClass=="5":
            if "정보" in sub:
                return "선택 A"
            elif "기하" in sub:
                return "선택 C"
            elif "물리학" in sub:
                return "선택 D"
            elif "중국어" in sub:
                return "선택 E"
            elif "화학" in sub:
                return "선택 F"

        elif schlClass=="6":
            if "생명" in sub:
                return "선택 A"
            elif "세계지리" in sub:
                return "선택 C"
            elif "기하" in sub:
                return "선택 D"
            elif "고전문학" in sub:
                return "선택 E"
            elif "정보" in sub:
                return "선택 F"

        elif schlClass=="7":
            if "지구과학" in sub:
                return "선택 A"
            elif "일본어" in sub:
                return "선택 C"
            elif "화학" in sub:
                return "선택 D"
            elif "물리학" in sub:
                return "선택 E"
            elif "고전문학" in sub:
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
            if "생활과" in sub:
                return "선택 A"
            elif "물리학" in sub:
                return "선택 C"
            elif "지구과학" in sub:
                return "선택 D"
            elif "기하" in sub:
                return "선택 E"
            elif "윤리와" in sub:
                return "선택 F"

        elif schlClass=="10":
            if "기하" in sub:
                return "선택 A"
            elif "화학" in sub:
                return "선택 C"
            elif "중국어" in sub:
                return "선택 D"
            elif "생활과" in sub:
                return "선택 E"
            elif "지구과학" in sub:
                return "선택 F"
    """
    try:
        return subjectData[grade][schlClass][sub]
    except KeyError:
        return sub



def getSchedul(officeCode, schlCode, grade, schlClass, date, dateRange):
    year = int(date[0:4])
    month = int(date[4:6])
    day = int(date[6:8])
    weekday = datetime.date(year, month, day).weekday()

    dateFrom = datetime.datetime(year, month, day)
    dateTo = datetime.datetime(year, month, day)

    if dateRange=="day":
        pass

    elif dateRange=="week":
        dateFrom -= datetime.timedelta(days=weekday)
        dateTo += datetime.timedelta(days=(4-weekday))
        if 4<weekday:
            dateFrom += datetime.timedelta(days=7)
            dateTo += datetime.timedelta(days=7)

    dateFrom = dateFrom.strftime("%Y%m%d")
    dateTo = dateTo.strftime("%Y%m%d")


    url = f"https://open.neis.go.kr/hub/hisTimetable?KEY={neisKey}&Type=json"
    url += f"&Type=json"
    url += f"&ATPT_OFCDC_SC_CODE={officeCode}"
    url += f"&SD_SCHUL_CODE={schlCode}"
    url += f"&GRADE={grade}"
    url += f"&CLASS_NM={schlClass}"
    url += f"&TI_FROM_YMD={dateFrom}&TI_TO_YMD={dateTo}"

    print(url)

    context = ssl._create_unverified_context()
    request = ul.Request(url)
    response = ul.urlopen(request, context=context)

    if response.getcode()==200:
        responseData = response.read()
        responseData = json.loads(responseData)
        try:
            if responseData["RESULT"]["MESSAGE"]=="해당하는 데이터가 없습니다.":
                #print("code : 404")
                return json.dumps({"code":404, "header":{"dateFrom":dateFrom, "dateTo":dateTo}})
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
        #print(f"code : {response.getcode()}")
        return json.dumps({"code":response.getcode()})