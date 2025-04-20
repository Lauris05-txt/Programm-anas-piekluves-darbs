import freecurrencyapi
import sqlite3
import hashlib

class Api():
    def __init__(self):
        self.admin = freecurrencyapi.Client('fca_live_lNvhPRSZ6CKfTPB5Va8WVFLfFlQHGEbv2XGXr84p')
        self.result = None
        
    def get_currency_data(self, currency):
        result = self.admin.latest(base_currency=currency)
        return result

    def convert_currency(self, input_currency, output_currency):
        response = self.get_currency_data(input_currency)
        # try:
        return response["data"][output_currency]
        # except:
        #     KeyError

class Database():
    def __init__(self):
        self.connection = sqlite3.connect('valutas_konvertetajs.db')
        self.cur = self.connection.cursor()

    def insert_conversion_history(self, user_id, value_from, currency_from, value_to, currency_to, date, time):
        self.cur.execute("""INSERT INTO 'conversion_history'('user_id', 'value_from', 'currency_from', 'value_to', 'currency_to', 'date', 'time') VALUES (?, ?, ?, ?, ?, ?, ?)
""", (user_id, value_from, currency_from, value_to, currency_to, date, time))
        self.connection.commit()
        self.connection.close()

    def get_user_data_by_id(self, user_id):
        self.cur.execute("""SELECT * FROM 'user' WHERE user_id=(?)""", (user_id,))
        user = self.cur.fetchone()
        print("utr")
        self.connection.close()
        return user

    def get_user_data_by_username(self, username):
        self.cur.execute("""SELECT * FROM 'user' WHERE username=(?)""", (username,))
        user = self.cur.fetchone()
        self.connection.close()
        return user
    
    def get_histrory(self, user_id):
        self.cur.execute("""SELECT * FROM 'conversion_history' WHERE user_id=(?)""", (user_id,))
        history = self.cur.fetchall()
        self.cur.close()
        return history[-11:]
    
    def delete_history(self, user_id):
        self.cur.execute("""DELETE FROM 'conversion_history' WHERE user_id=(?)""", (user_id,))
        self.connection.commit()
        self.cur.close()
        return (("", "", "", "", "", "", ""))

    def user_data(self, username, email, password):
        hashed_password = hashlib.md5(password.encode()).hexdigest()
        self.cur.execute("""INSERT INTO 'user'('username', 'email', 'password') VALUES (?, ?, ?) """, (username, email, hashed_password))
        self.connection.commit()
        self.connection.close()

    def login(self, username, password):
        self.cur.execute("""SELECT * FROM 'user' WHERE username=(?)""", (username,))
        user = self.cur.fetchone()
        print(user)
        if user:
            hashed_password = hashlib.md5(password.encode()).hexdigest()
            
            if hashed_password == user[3]:
                return True
            else:
                return False
            
        else:
            return False
