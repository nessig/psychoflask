from app import db

cursor = db.postgres_connection.get_cursor()
# users = 
cursor.execute("SELECT * FROM posts")
print "otherstuff"
print cursor.fetchone()
cursor.close()
