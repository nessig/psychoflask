# db.py
import psycopg2
import app
from contextlib import closing
# class PostgresConnection(object):

#     def __init__(self):
#         self.connection = None

#     def init_app(self, app):
#         self.connection = psycopg2.connect(app.config["DSN"])

#         @app.teardown_appcontext
#         def close_connection(response_or_exception):
#             self.connection.close()
#             return response_or_exception

#     def get_cursor(self):
#         if not self.connection:
#             raise RuntimeError('Attempt to get_cursor on uninitialized connection')
#         return self.connection.cursor()

# postgres_connection = PostgresConnection()


def connect_db():
    return psycopg2.connect(database=app.config['DATABASE'],
                            user=app.config['USERNAME'],
                            password=app.config['PASSWORD'])


def init_db():
    with closing(connect_db()) as conn, conn.cursor() as cursor:
        with app.open_resource('query.sql', mode='r') as f:
            cursor.execute(f.read())
        conn.commit()
