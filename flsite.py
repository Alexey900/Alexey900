import sqlite3 as sq
##changes

params = [  # values
    ("Alexey", "Bondarev", 1),
    ("Mary", "Ivanova", 2),
    ("Michael", "Beshnev", 1),
    ("Vlad", "Vladov", 1),
    ("Ludmila", "Borisovna", 2),
    ("Kristina", "Kotova", 2),

]

try:
    cn = sq.connect("flsite.db")  # connect with database if exists else create
    cur = cn.cursor()             # get a cursor to read data

    # create table employee
    cur.execute("""CREATE TABLE IF NOT EXISTS employee (
                   id INTEGER PRIMARY KEY,
                   first VARCHAR(50) NOT NULL,
                   surname VARCHAR(50) NOT NULL,
                   gender INTGERE DEFAULT 1
                   ); """)

    # ? the number means the index of the list items
    cur.executemany("INSERT INTO employee VALUES(NULL, ?, ?, ?)", params)
    cur.executescript(r"""
                        BEGIN;
                        UPDATE employee SET firs56t = '99999' 
                        WHERE surname LIKE '%a';
                        """)
    
    cn.commit()

except sq.Error as error:
    if cn:
        cn.rollback()       # if founded error than do rollback
    print("Catched error:  ", error)

finally:
    if cn:
        cn.close()
