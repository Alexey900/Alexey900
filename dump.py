import sqlite3 as sq
import unittest as un
from os import path

try:
    bd = sq.connect("flsite_2.db")     # open fliste.db file
    cur = bd.cursor()                # get cursor

    with open(r"sql_dump.sql", "w") as file:     # create new sql_dump.sql file

        for sql in bd.iterdump():              # get each line bd
            file.write(sql)                     # write gotten value

except IOError as error:             # if not founded file or can't open
    print("Can't open file: " + error)

finally:
    bd.close()                       # close connect


class Test(un.TestCase):
    """Unittest to check if file exists"""
    def test_exists(self):
        self.assertEqual(path.exists("flsite.db"), True)


if __name__ == "__main__":
    un.main()                        # start checking


input("end")
