'''
Created on Jan 10, 2017

@author: hanif
'''

import pymysql


class Database:
    def connect(self):
        # return pymysql.connect("phonebook-mysql", "dev", "dev", "crud_flask")

        return pymysql.connect(host="localhost", user="root", password="password", database="easytimepro", charset='utf8mb4')

    def read(self, date):
        con = Database.connect(self)
        cursor = con.cursor()

        try:
            if date == None:
                cursor.execute("SELECT emp_code,punch_time,terminal_alias FROM iclock_transaction order by emp_code asc")
            else:
                cursor.execute(
                    "SELECT emp_code,punch_time,terminal_alias FROM iclock_transaction where date(punch_time) between %s and %s order by emp_code asc", (date,date))

            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close()
