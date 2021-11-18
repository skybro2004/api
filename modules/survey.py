import sqlite3



con = sqlite3.connect("../resources/serveyData.db", check_same_thread=False)
cur = con.cursor()



def getSurvey():
    pass

def storeSurvey():
    pass