import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="yashghongade.mysql.pythonanywhere-services.com",
        user="yashghongade",
        password="Yash@1109",
        database="yashghongade$society"
    )

print("Connected!")