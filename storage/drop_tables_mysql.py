import mysql.connector
db_conn = mysql.connector.connect(host="tom6.westus2.cloudapp.azure.com", user="root",
                                  password="aaa", database="events")
db_cursor = db_conn.cursor()
db_cursor.execute('''
 DROP TABLE delivery_order, pickup_order
''')
db_conn.commit()
db_conn.close()
