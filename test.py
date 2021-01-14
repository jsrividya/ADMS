import mysql.connector


def connect_to_db():
    mydb = mysql.connector.connect(
      host="mydbinstance.clv2txpsdfyb.us-east-1.rds.amazonaws.com",
      user="admin",
      passwd="Mani1232",
      database="ORCL",
      port=1521
    )
    mycursor = mydb.cursor()



connect_to_db()