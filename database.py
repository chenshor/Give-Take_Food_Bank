import datetime
import sqlite3
from sqlite3 import Error

class DataBase:
    """ This function opens the connection and creates (if does not exists) a database"""
    def __init__(self):
        """Creating a connection"""
        self.conn = sqlite3.connect('database.db')

        """Creating a cursor object"""
        self.cur = self.conn.cursor()

        """Performing a query, commit and close"""

        ## checks if the tables already exists
        check_if_exists = self.cur.execute(
            ''' SELECT count(*) FROM sqlite_master WHERE type='table' AND name='users' ''')
        if check_if_exists.fetchone()[0] != 1:
            self.cur.execute("CREATE TABLE IF NOT EXISTS users ("
                             " UserName MESSAGE_TEXT,"
                             " Password MESSAGE_TEXT,"
                             " Email MESSAGE_TEXT)")


        check_if_exists = self.cur.execute(
            ''' SELECT count(*) FROM sqlite_master WHERE type='table' AND name='dataTable' ''')
        if check_if_exists.fetchone()[0] != 1:
            self.cur.execute("CREATE TABLE IF NOT EXISTS dataTable ("
                             " ItemName MESSAGE_TEXT,"
                             " Amount INTEGER,"
                             " Category MESSAGE_TEXT,"
                             " Location MESSAGE_TEXT,"
                             " UserName MESSAGE_TEXT,"
                             "Taken MESSAGE_TEXT)")

        self.conn.commit()
        self.conn.close()  # closes the connection

        # self.filename = filename
        self.user = None
        # self.file = None
        # self.load()

    # def load(self):
    #     self.file = open(self.filename, "r")
    #     self.users = {}
    #
    #     for line in self.file:
    #         email, password, name, created = line.strip().split(";")
    #         self.users[email] = (password, name, created)
    #
    #     self.file.close()

    def get_user(self, user):
        if user==self.user[0][0]:
            return self.user[0]
        else:
            return -1

    def add_user(self, email, password, name):
        self.conn = sqlite3.connect('database.db')
        self.cur = self.conn.cursor()
        #check if exist
        self.cur.execute("SELECT * FROM users WHERE UserName=?",(name,))
        result = self.cur.fetchall()
        if len(result) > 0:
            -1
        self.cur.execute("INSERT INTO users (UserName, Password, Email) VALUES (?, ?, ?);",(name, password, email))
        self.conn.commit()
        self.conn.close()
        return 1;

    def validate(self, name, password):
        self.conn = sqlite3.connect('database.db')
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT * FROM users WHERE UserName=? AND Password=?", (name, password))
        result = self.cur.fetchall()
        if len(result) == 0:
            return False;
        self.user=result
        return True;


    """ This function adds a new item to the dataTable"""
    """ Returns true if the insertion succeed, otherwise false"""
    def add_item_to_user(self, name, item_name, amount, location,category):
        self.conn = sqlite3.connect('database.db')
        self.cur = self.conn.cursor()
        self.cur.execute("INSERT INTO dataTable (ItemName,Amount,Category,Location,UserName,Taken) VALUES (?, ?, ?,?,?,?);",
                         (item_name,amount,category,location,name,"FALSE"))
        self.conn.commit()
        self.cur.execute("SELECT * FROM dataTable WHERE UserName=? AND ItemName=?", (name, item_name))
        result = self.cur.fetchall()
        self.conn.close()
        if len(result) == 0:
            return False
        return True

    def update_taken (self, name, item_name,taken):
        self.conn = sqlite3.connect('database.db')
        self.cur = self.conn.cursor()
        self.cur.execute("UPDATE dataTable SET Taken =? WHERE UserName=? AND ItemName=? "
                         "VALUES (?, ?, ?);",
                         (taken,name,item_name))
        self.conn.commit()
        self.cur.execute("SELECT Taken FROM dataTable WHERE UserName=? AND ItemName=?", (name, item_name))
        result = self.cur.fetchall()
        self.conn.close()
        if (result[0]==taken):
            return  True
        else:
            return False


    def get_posts_by_user(self, userName):
        self.conn = sqlite3.connect('database.db')
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT * FROM dataTable WHERE UserName=?", (userName))
        self.conn.commit()
        posts = self.cur.fetchall()
        self.conn.close()
        return posts

    def save(self):
        with open(self.filename, "w") as f:
            for user in self.users:
                f.write(user + ";" + self.users[user][0] + ";" + self.users[user][1] + ";" + self.users[user][2]
                        + ";" + self.users[user][3] + ";" + self.users[user][4]
                        + "\n")

    def search(self, category, location):
        self.conn = sqlite3.connect('database.db')
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT * FROM dataTable WHERE Category=? AND Location=?",
                         (category, location))
        result = self.cur.fetchall()

        if len(result) == 0:
            return "no results"
        return result

    def update(self,userName, itemName, amount, location):
        try:
            self.conn = sqlite3.connect('database.db')
            self.cur = self.conn.cursor()
            self.cur.execute("UPDATE dataTable SET Amount =?, Location=? WHERE UserName=? AND ItemName=? ",
                                 (amount, location, userName,itemName))
            self.conn.commit()
            self.conn.close()
            return True
        except:
            return False

