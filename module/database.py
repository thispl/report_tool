'''
Created on Jan 10, 2017

@author: hanif
'''

import pymysql


class Database:
    def connect(self):
        # return pymysql.connect("phonebook-mysql", "dev", "dev", "crud_flask")

        return pymysql.connect(host="localhost", user="root", password="password", database="crud_flask", charset='utf8mb4')

    def read(self, id):
        con = Database.connect(self)
        cursor = con.cursor()

        try:
            if id == None:
                cursor.execute("SELECT * FROM daily_food_entry order by employee asc")
            else:
                cursor.execute(
                    "SELECT * FROM daily_food_entry where employee = %s order by employee asc", (id,))

            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close()

    def insert(self, data):
        con = Database.connect(self)
        cursor = con.cursor()

        try:
            cursor.execute("INSERT INTO daily_food_entry(employee,item,price,date,time,is_subsidy,is_synced) VALUES(%s, %s, %s,CURDATE(), NOW(), '0', '0')",
                           (data['employee'], data['item'], data['price']))
            con.commit()

            return True
        except:
            con.rollback()

            return False
        finally:
            con.close()

    def update(self, id, data):
        con = Database.connect(self)
        cursor = con.cursor()

        try:
            cursor.execute("UPDATE phone_book set name = %s, phone = %s, address = %s where id = %s",
                           (data['name'], data['phone'], data['address'], id,))
            con.commit()

            return True
        except:
            con.rollback()

            return False
        finally:
            con.close()

    def delete(self, id):
        con = Database.connect(self)
        cursor = con.cursor()

        try:
            cursor.execute("DELETE FROM phone_book where id = %s", (id,))
            con.commit()

            return True
        except:
            con.rollback()

            return False
        finally:
            con.close()
