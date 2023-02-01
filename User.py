class UserInfo:
    def __init__(self, name, db):
        self.__user = db.getUserId(name)
        self.__db = db
        self.name = self.__user[1]

    def is_authenticated(self):
        if self.__user:
            return True
        else:
            return False

    def getAvatar(self, rootPath):
        try:
            if not self.__db.getAll(self.__user[0])[3]:
                with open(rootPath + "\\static\\images\\default.png", 'rb') as file:
                    img = file.read()
                return img
        except Exception as error:
            print('Найдена ошибка ', error)
        img = self.__db.getAll(self.__user[0])[3]

        return img

    def is_active(self):
        return True

    def get_id(self):
        return str(self.__user[1])

    def get_ID(self):
        return str(self.__user[0])

    def is_anonymous(self):
        return False
