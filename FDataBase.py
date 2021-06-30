class FDataBase():
    def __init__(self,db):
        self.__db = db
        self.__cur = db.cursor()

    def getValues(self):
        sql = ''' GET * FROM data'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res : return res
        except:
            print('error read database')
        return []
