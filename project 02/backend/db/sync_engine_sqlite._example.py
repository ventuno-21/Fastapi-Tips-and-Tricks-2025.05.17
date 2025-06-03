import sqlite3


connection = sqlite3.connect("myExampleSqlite2.db")
cursor = connection.cursor()

# create a table
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS shipment
    (id INTEGER PRIMARY KEY , content TEXT, weight REAL, status TEXT)
    """
)


# # How to add data to out shipment table => You have to commit after insert a data to database
# cursor.execute("INSERT INTO shipment  VALUES (12071 ,'MY TEXT',  8.5, 'placed')")
# connection.commit()


# How to fetch a data from a table
cursor.execute("SELECT id, content, weight FROM shipment ")
result = cursor.fetchall()
print(result)

# # Delete a data from database
# cursor.execute("DELETE From shipment WHERE id = 12071")
# connection.commit()


# Update
# cursor.execute("Update shipment SET status = 'in treansit' WHERE id=12071")
# connection.commit()


# # Update
# id=12071
# status='placed'
# cursor.execute(f"Update shipment SET status = '{status}' WHERE id={id}")
# connection.commit()


# # Drop a table
# cursor.execute("DROP TABLE shipment")
# connection.commit()


connection.close()
