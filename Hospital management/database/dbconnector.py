
import mysql.connector


def get_connector():

    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Nopassword@20135748",
            database="hospitaltests"
        )

        if mydb.is_connected():
            print("Connected to the database:", mydb.database)

        return mydb  # IMPORTANT: Return connection

    except mysql.connector.Error as e:
        print("Database connection error:", e)
        return None
