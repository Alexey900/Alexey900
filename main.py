import sqlite3 as sq

cars = [
    ["Audi", 3232.21],
    ["Volkswagen", 3232.21],
    ["Skoda", 3232.21],
    ["LADA", 3232.21],
    ["BMW", 3232.21]
]

con = None
try:
    con = sq.connect("saper.db")
    cur = con.cursor()  # Cursor
    # cur.execute("""DROP TABLE users""")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS cars (
        id INTEGER,
        model TEXT,
        price NUMERICIC NOT NULL
    );
    """)
    cur.executemany("INSERT INTO cars VALUES(NULL, ?, ?)", cars)

    cur.executescript("""
    BEGIN;
    UPDATE cars SET id = 1 WHERE model = 'Audi';
    UPDATE cars SET id = 2 WHERE model = 'Volkswagen';
    UPDATE cars SET id = 3 WHERE model = 'Skoda';
    UPDATE cars3 SET id = 4 WHERE model = 'LADA';
    UPDATE cars SET id = 5 WHERE model = 'BMW';
    """)
    con.commit()


except sq.Error as error:
    if con:
        con.rollback()
    print("Eroor: ", error)

finally:
    if con:
        con.close()
