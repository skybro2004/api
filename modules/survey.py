import sqlite3
import json




def getSurvey(date):
    year = date[0:4]
    month = date[4:6]
    day = date[6:8]
    con = sqlite3.connect(f"./resources/serveyData/{year[2:]}-{month}.db")
    cur = con.cursor()

    try:
        cur.execute(f"SELECT * FROM day{day}")
    except sqlite3.OperationalError:
        return 404


    index = 0
    qualSum = [0, 0, 0, 0, 0]
    quanSum = [0, 0, 0, 0, 0]
    rates = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
    for data in cur.fetchall():
        qualSum[data[0] + 2] += 1
        quanSum[data[1] + 2] += 1
        temp = list(map(int, data[2].split(".")))
        rates[temp[0]][0] += 1
        rates[temp[0]][1] += temp[1]

        index += 1

    for i, value in enumerate(rates):
        if value[0]==0:
            rates[i] = -1
        else:
            rates[i] = round(value[1]/value[0], 2)

    
    return {"index":index, "quality":qualSum, "quantity":quanSum, "menuRate":rates}





def storeSurvey(date, value):
    year = date[0:4]
    month = date[4:6]
    day = date[6:8]

    con = sqlite3.connect(f"./resources/serveyData/{year[2:]}-{month}.db")
    cur = con.cursor()
    cur.execute(f"CREATE TABLE IF NOT EXISTS day{day}(quality INTEGER, quantity INTEGER, menuRate TEXT)")

    cur.execute(f"INSERT INTO day{day} VALUES ({value['quality']}, {value['quantity']}, {str(value['mealIndex']) + '.' + str(value['mealRate'])})")

    con.commit()
    con.close()

    return 0




if __name__=="__main__":
    storeSurvey("20211123", {
        "quality":0,
        "quantity":2,
        "mealIndex":1,
        "mealRate":4
    })

    print(getSurvey("20211123"))