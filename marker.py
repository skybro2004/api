import sqlite3

con = sqlite3.connect("answerSheet.db")
cur = con.cursor()

def getAll():
    res = []
    cur.execute("SELECT * FROM sheets")
    for item in cur.fetchall():
        res.append({"id":item[0], "name":item[1]})
    return res

def getSheet(sheetId):
    res = {}
    cur.execute(f"SELECT * FROM {sheetId}")
    for item in cur.fetchall():
        res[item[0]] = item[1]
    return res

        
if __name__=="__main__":
    print(getAll())
    print(getSheet("H22109SSB1P1"))