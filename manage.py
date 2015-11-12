from flask.ext.script import Manager

from app import app, init_db
# app = Flask(__name__)
# configure your app


# insertUserSQL = """
# insert into users (username, email, password)
# values (%s, %s, %s);
# """

# insertPostSQL = """
# insert into posts (title, body, author_id, pub_date)
# values (%s, %s, %s,%s);
# """

# selectIdFromUsernameSQL = """
# select id from users where username=%s;
# """

# userData1 = ("nessig", "nessig@mit.edu", "123")
# userData2 = ("nolan", "nolan@example.com", "123")
# # postData1 = ("My First Post!", "This is the body of my first post!", 1)


# init_db()


# def dbExecuteFetch(SQL, data):
#     with closing(connect_db()) as conn, conn.cursor() as cur:
#         cur.execute(SQL, data)
#         results = cur.fetchall()
#     return results


# def dbExecuteCommit(SQL, data):
#     with closing(connect_db()) as conn, conn.cursor() as cur:
#         cur.execute(SQL, data)
#         conn.commit()

# dbExecuteCommit(insertUserSQL, userData1)
# dbExecuteCommit(insertUserSQL, userData2)


# userId = dbExecuteFetch(selectIdFromUsernameSQL, ("nessig",))[0]
# postData1 = ("My First Post!", "This is the body of my first post!", userId, datetime.utcnow())
# postData2 = ("My Second Post!", "This is the body of my second post!", userId, datetime.utcnow())
# postData3 = ("My Third Post!", "This is the body of my third post!", userId, datetime.utcnow())
# dbExecuteCommit(insertPostSQL, postData1)
# dbExecuteCommit(insertPostSQL, postData2)
# dbExecuteCommit(insertPostSQL, postData3)


manager = Manager(app)


@manager.command
def initdb():
    print "Initializing database"
    init_db()


if __name__ == "__main__":
    manager.run()
