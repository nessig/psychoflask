from flask import Flask, render_template, g, redirect, url_for, flash, session
# import db
import psycopg2
import psycopg2.extras
from contextlib import closing
from forms import LoginForm, RegisterForm
from functools import wraps

# configuration
DATABASE = 'flaskr'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'nessig'
PASSWORD = '123'

DSN = "dbname=%s user=%s password=%s" % (DATABASE, USERNAME, PASSWORD)

app = Flask(__name__)
app.config.from_object(__name__)
# do some other stuff
# db.postgres_connection.init_app(app)


def connect_db():
    return psycopg2.connect(database=app.config['DATABASE'],
                            user=app.config['USERNAME'],
                            password=app.config['PASSWORD'])


def init_db():
    with closing(connect_db()) as conn, conn.cursor() as cursor:
        with app.open_resource('query.sql', mode='r') as f:
            cursor.execute(f.read())
        conn.commit()


insertUserSQL = """
insert into users (username, email, password)
values (%s, %s, %s);
"""

insertPostSQL = """
insert into posts (title, body, author_id)
values (%s, %s, %s);
"""

selectIdFromUsernameSQL = """
select id from users where username=%s;
"""

userData1 = ("nessig", "nessig@mit.edu", "123")
userData2 = ("nolan", "nolan@example.com", "123")
# postData1 = ("My First Post!", "This is the body of my first post!", 1)


init_db()


def dbExecuteFetch(SQL, data):
    with closing(connect_db()) as conn, conn.cursor() as cur:
        cur.execute(SQL, data)
        results = cur.fetchall()
    return results


def dbExecuteCommit(SQL, data):
    with closing(connect_db()) as conn, conn.cursor() as cur:
        cur.execute(SQL, data)
        conn.commit()

dbExecuteCommit(insertUserSQL, userData1)
dbExecuteCommit(insertUserSQL, userData2)


userId = dbExecuteFetch(selectIdFromUsernameSQL, ("nessig",))[0]
postData1 = ("My First Post!", "This is the body of my first post!", userId)
dbExecuteCommit(insertPostSQL, postData1)


# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap


@app.before_request
def before_request():
    g.db = connect_db()
    print "connected to :"
    print g.db


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()
        print "disconnected from:"
        print db


@app.route("/")
def index():
    cur = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("select * from users;")
    users = cur.fetchall()
    posts = []
    user_ids = [user["id"] for user in users]
    cur.execute("select * from posts where author_id=ANY(%s)", (user_ids,))
    posts = cur.fetchall()
    # print posts
    cur.close()
    return render_template("index.html",
                           users=users,
                           posts=posts)


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        cur = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        userData = (form.username.data, form.email.data, form.password.data)
        insertUserSQL = """
        insert into users (username, email, password)
        values (%s,%s,%s);
        """
        cur.execute(insertUserSQL, userData)
        g.db.commit()
        cur.close()
        return redirect(url_for('index'))
    return render_template('register.html',
                           form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        cur = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cur.execute('select * from users where username=%s and password=%s',
                        (username, password))
            user = cur.fetchone()
            if user is not None:
                login_user(user)
                flash('You were logged in, %s. Go Crazy.' % (username))
                print "Current user is: " + str(g.current_user)
                return redirect(url_for('index'))
            else:
                flash("Invalid username and/or password.")
        except psycopg2.DatabaseError, e:
            flash('Error %s' % e)
        cur.close()
    return render_template('login.html', form=form)


def login_user(user):
    session["user_id"] = user["id"]


@app.before_request
def load_user():
    if "user_id" in session:
        cur = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("select * from users where id=%s;", (session["user_id"],))
        user = cur.fetchone()
        cur.close()
    else:
        user = None
    g.current_user = user


@app.route('/logout')
@login_required
def logout():
    session.pop('user_id', None)
    flash('You were logged out')
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run()
