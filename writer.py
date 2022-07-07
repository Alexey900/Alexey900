import sqlite3 as sq


data = [
    ("Misha", "Безымянный.jpg"),
    ("Yuri", "Безымянный.jpg"),
    ("Maria", "Безымянный.jpg"),
]


def avaLoad(name):
    try:
        ava = open(rf"C:\Users\ПК\Desktop\{name}", "rb")
        return ava.read()
    except IOError as error:
        print("Can't open: ", error)
        return False


with sq.connect("flsite_2.db") as cn:
    cn.row_factory = sq.Row
    cur = cn.cursor()
    cur.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        name VARCHAR,
        ava BLOB,
        id INTEGER PRIMARY KEY
    );
    """)
    for items in data:
        if avaLoad(items[1]):
            img = sq.Binary(avaLoad(items[1]))
            cur.execute("INSERT INTO users VALUES(?, ?, NULL)", (items[0], img))