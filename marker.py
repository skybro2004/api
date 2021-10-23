import re
import sqlite3
import json

con = sqlite3.connect("answerSheet.db", check_same_thread=False)
cur = con.cursor()

def getAll(studGrade, studClass):
    res = []
    cur.execute(f"SELECT * FROM sheets WHERE grade = \"{studGrade}\" and class = \"{studClass}\"")
    for item in cur.fetchall():
        res.append({"id":item[0], "name":item[1], "index":json.loads(item[4])})
    return res

def getSheet(sheetId, index):
    if index==0:
        res = []
        cur.execute(f"SELECT indexes FROM sheets WHERE id = \"{sheetId}\"")
        #return json.loads(cur.fetchall())
        for item in cur.fetchall()[0]:
            print(item)
            res.append(json.loads(item))
        return res


    res = {}
    cur.execute(f"SELECT * FROM {sheetId}P{index}")
    for item in cur.fetchall():
        res[item[0]] = json.loads(item[1])
    return res

        
if __name__=="__main__":
    print(getAll("H2", "J10"))
    print(getSheet("H22109SSB1P1"))