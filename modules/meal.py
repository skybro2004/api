import urllib.request as ul
import ssl
import json, re

neisKey = "028278aaacd242438668d46a5464e934"



def getMeal(officeCode, schlCode, date):
    year = int(date[0:4])
    month = int(date[4:6])
    day = int(date[6:8])

    url = f"https://open.neis.go.kr/hub/mealServiceDietInfo?KEY={neisKey}&Type=json"
    url += f"&ATPT_OFCDC_SC_CODE={officeCode}"
    url += f"&SD_SCHUL_CODE={schlCode}"
    url += f"&MLSV_FROM_YMD={date}&MLSV_TO_YMD={date}"

    context = ssl._create_unverified_context()
    request = ul.Request(url)
    response = ul.urlopen(request, context=context)
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
            meal = re.sub('[(][0-9][)]', '', meal)
            allergy = re.findall(r'[0-9]+[.]', meal)
            for i in range(len(allergy)):
                allergy[i] = allergy[i].replace(".", "")
            meal = re.sub('[0-9]+[.]', '', meal)
            meals.append({"name":meal, "allergy":allergy})
        Calorie = responseData["CAL_INFO"]
        print(meals)
        return json.dumps({"code":200, "meal":meals, "cal":Calorie})

    else:
        return json.dumps({"code":response.getcode()})