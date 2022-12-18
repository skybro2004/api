import json


dataPath = "/home/sj/api/crosswalk/data.json"



def parseJsonData():
    try:
        with open(dataPath) as file:
            return json.load(file)
    except FileNotFoundError:
        with open(dataPath, "w") as file:
            file.write("{}")
            return "{}"



def getCrosswalkPos(dateFrom, dateTo):
    data_origin = parseJsonData()
    data = []

    for date in range(int(dateFrom), int(dateTo)+1):
        try:
            data += data_origin[str(date)]
        except KeyError:
            continue

    return json.dumps(data)



def addCrosswalkPos(date, json_str):
    data_origin = parseJsonData()
    data = json.loads(json_str)
    print(type(data_origin))
    print(data)

    try:
        data_origin[date].append(data)
    except KeyError:
        data_origin[date] = [data]

    print(json.dumps(data_origin))

    with open(dataPath, "w") as file:
        file.write(json.dumps(data_origin, indent=4))



if __name__=="__main__":
    # print(parseJsonData())
    # addCrosswalkPos("20221218", '{"pos":[12, 34]}')
    print(getCrosswalkPos("20221217", "20221217"))