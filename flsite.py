import sqlite3 as sq


try:
    cn = sq.connect("flsite.db")
    cur = cn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS employee (
                   id INTEGER PRIMARY KEY,
                   first VARCHAR(50) NOT NULL,
                   surname VARCHAR(50) NOT NULL,
                   gender INTGERE DEFAULT 1
                   ); """)

except sq.Error as error:
    print("Cathced error:  ", error)

finally:
    if cn:
        cn.close()
