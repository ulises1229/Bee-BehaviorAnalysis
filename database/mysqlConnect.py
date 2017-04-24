import mysql.connector
from mysql.connector import errorcode

class mysqlConnect:
    def __init__(self):
        """ Initialization Code """

    def connectDB(self):
        # FIXME: Read the credentials from a file
        try:
            con = mysql.connector.connect(user="root", password="so1di2ba3",
                                    host= "localhost", database = "bees")

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:
            return con

    def insertData(self):
        con = self.connectDB()
        cursor = con.cursor()

        cursor.execute("select * from bees.site")

        #for i in cursor:
            #print i

        con.close()

