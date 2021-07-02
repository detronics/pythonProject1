import  sqlite3
from datetime import date
class FDataBase:
    def __init__(self,db):
        self.__db = db
        self.__cur = db.cursor()

    def getValues(self):
        sql = '''SELECT * FROM data'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res : return res
        except:
            print('error read database')
        return []

    def addValue(self, sat_value):
        try:
            data = date.today()
            self.__cur.execute('INSERT INTO data VALUES(NULL, ?, ?)', (data, sat_value))
            self.__db.commit()
        except sqlite3.Error as e:
            print('add error' + str(e))
            return False
        return True


