from flask import url_for


class UserLogin():
    def fromDB(self, user_id, db):
        self.__user = db.getUser(user_id)
        return self

    def create(self, user):
        self.__user = user
        return self

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymus(self):
        return False

    def get_id(self):
        return str(self.__user['id'])

    def get_name(self):
        return str(self.__user['name'])

    def get_subname(self):
        return str(self.__user['subname'])

    def get_cognomen(self):
        return str(self.__user['cognomen'])

    def get_age(self):
        return str(self.__user['age'])

    def get_weight(self):
        return str(self.__user['weight'])

    def get_height(self):
        return str(self.__user['height'])

    def getAvatar(self, app):
        img = None
        if not self.__user['avatar']:
            try:
                with app.open_resource(app.root_path + url_for('static',filename='images/avatar.jpg'), 'rb') as f:
                    img = f.read()
            except FileNotFoundError as e:
                print('Не найден аватар по умолчанию',str(e))
        else:
            img = self.__user['avatar']

        return img

    def verifyExt(self, filename):
        ext = filename.split('.',1)[1]
        if ext == "JPG" or ext == 'jpg':
            return True
        return False