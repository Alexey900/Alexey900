from msilib.schema import Error

from requests import delete


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def getMenu(self):
        try:
            self.__cur.execute("SELECT * FROM posts")
            res = self.__cur.fetchall()
            return res
        except BaseException as exp:
            print("Not found table posts or else error", exp)
        return []

    def addContent(self, content):
        try:
            self.__cur.executescript(f"""
            INSERT INTO posts VALUES(
                        NULL, "{content['authour'] if content['authour'] else 'NULL'}",
                        "{content["title"]}", "{content["content"]}")""")
            return 200
        except BaseException as error:
            print("catched error", error)

    def getPost(self, post_id):
        try:
            self.__cur.execute(f"SELECT * FROM posts WHERE id = {post_id}")
            if self.__cur.fetchone():
                self.__cur.execute(f"SELECT * FROM posts WHERE id = {post_id}")
                return self.__cur.fetchone()
        except:
            print("Error with getPost method")

    def deletePost(self, post_id):
        self.__cur.execute(f"DELETE FROM posts WHERE id = {post_id}")
        self.__db.commit()
