import sqlite3
from datetime import date


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def getValues(self):
        sql = '''SELECT * FROM data'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: return res
        except:
            print('error read database')
        return []

    def addValue(self, sat_value):
        try:
            data = date.today()
            self.__cur.execute('INSERT INTO data VALUES(NULL, ?, ?)', (data, sat_value))
            self.__db.commit()
        except sqlite3.Error as e:
            print('add error ' + str(e))
            return False
        return True

    def addUser(self, login, psw_hash, name, subname, cognomen, age, weight, height):
        try:
            self.__cur.execute(f'SELECT COUNT() as "count" FROM users WHERE login LIKE "{{login}}"')
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print('login is busy')
                return False
            self.__cur.execute('INSERT INTO users VALUES(NULL, ?, ?, ?, ?, ?, ?, ?, ?)',
                               (login, psw_hash, name, subname, cognomen, age, weight, height))
            self.__db.commit()
        except sqlite3.Error as e:
            print('add error ' + str(e))
            return False
        return True

    def getUser(self, user_id):
        try:
            self.__cur.execute(f'SELECT * FROM users WHERE id = {user_id} LIMIT 1')
            res = self.__cur.fetchone()
            if not res:
                print('user is not found')
                return False
            return res
        except sqlite3.Error as e:
            print('add error ' + str(e))
            return False

    def getUserbyLogin(self, login):
        try:
            self.__cur.execute(f'SELECT * FROM users WHERE login = {login} LIMIT 1')
            res = self.__cur.fetchone()
            if not res:
                print('user is not found')
                return False
            return res
        except sqlite3.Error as e:
            print('add error ' + str(e))
            return False
