from flask import Flask, render_template, g, redirect, url_for, flash, session
# import db
import psycopg2
import psycopg2.extras
from contextlib import closing
from datetime import datetime
from forms import LoginForm, RegisterForm, EditForm, PostForm
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

@app.template_filter()
def timesince(dt, default="just now"):
    """
    Returns string representing "time since" e.g.
    3 days ago, 5 hours ago etc.
    """

    now = datetime.utcnow()
    diff = now - dt
    
    periods = (
        (diff.days / 365, "year", "years"),
        (diff.days / 30, "month", "months"),
        (diff.days / 7, "week", "weeks"),
        (diff.days, "day", "days"),
        (diff.seconds / 3600, "hour", "hours"),
        (diff.seconds / 60, "minute", "minutes"),
        (diff.seconds, "second", "seconds"),
    )

    for period, singular, plural in periods:
        
        if period:
            return "%d %s ago" % (period, singular if period == 1 else plural)

    return default


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
insert into posts (title, body, author_id, pub_date)
values (%s, %s, %s,%s);
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
postData1 = ("My First Post!", "This is the body of my first post!", userId, datetime.utcnow())
postData2 = ("My Second Post!", "This is the body of my second post!", userId, datetime.utcnow())
postData3 = ("My Third Post!", "This is the body of my third post!", userId, datetime.utcnow())
dbExecuteCommit(insertPostSQL, postData1)
dbExecuteCommit(insertPostSQL, postData2)
dbExecuteCommit(insertPostSQL, postData3)


# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'user_id' in session and session["user_id"] != None:
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


# getFollowingPostsSQL = """
# select * from posts
# inner join followers
# on (author_id=following)
# where follower=%s
# order by pub_date desc;
# """


@app.route("/")
@login_required
def index():
    cur = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)

    getFollowingPostsSQL = """
select users.username,posts.title,posts.body,posts.pub_date from users
inner join posts
inner join followers
on (author_id=following)
on (users.id=author_id)
where follower=%s
order by pub_date desc;
"""
    cur.execute(getFollowingPostsSQL, (g.current_user['id'],))
    # users = cur.fetchall()
    
    # user_ids = [user["id"] for user in users]
    # cur.execute("select * from posts where author_id=ANY(%s)", (user_ids,))
    posts = cur.fetchall()
    # print posts
    cur.close()
    return render_template("index.html",
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


@app.route('/user/<username>', methods=['GET', 'POST'])
def user(username):
    form = PostForm()
    cur = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        cur.execute('select * from users where username=%s',
                    (username,))
        user = cur.fetchone()
        if user is not None:
            if form.validate_on_submit():
                title = form.title.data
                body = form.body.data
                author_id = user["id"]
                cur.execute('insert into posts (title,body,author_id,pub_date) values (%s,%s,%s,%s)',
                            (title, body, author_id,datetime.utcnow()))
                g.db.commit()
            isfollowing = is_following(g.current_user["id"], user["id"])
            cur.execute('select * from posts where author_id=%s',
                        (user['id'],))
            posts = cur.fetchall()
            return render_template('user.html',
                                   user=user,
                                   posts=posts,
                                   form=form,
                                   isfollowing=isfollowing)
        else:
            flash("User does not exist.")
    except psycopg2.DatabaseError, e:
        flash('Error %s' % e)
    cur.close()
    return redirect(url_for('index'))


@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    user = g.current_user
    form = EditForm()
    if form.validate_on_submit():
        text = form.text.data
        id = user["id"]
        cur = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute('update users set about_me=%s where id=%s', (text, id))
        g.db.commit()
        cur.close()
        return redirect(url_for('user', username=user["username"]))
    return render_template('edit.html', form=form)



@app.route('/follow/<username>')
@login_required
def follow(username):
    cur = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        cur.execute('select * from users where username=%s',
                    (username,))
        user = cur.fetchone()
        
        if user is None:
            flash("User %s could not be found" % username)
            return redirect(url_for('index'))
        if user == g.current_user:
            flash('You can\'t follow yourself!')
            return redirect(url_for('user', username=username))

        cur.execute('select * from followers where follower=%s and following=%s;',
                    (g.current_user["id"],user["id"]))
        
        u = cur.fetchone()
        print u
        if u is not None:
            flash('Already following ' + username + '.')
            return redirect(url_for('user', username=username))
        cur.execute('insert into followers values (%s,%s);', (g.current_user["id"],user["id"]))
        g.db.commit()
        cur.close()
        flash('You are now following ' + username + '!')
    except psycopg2.DatabaseError, e:
        flash('Error %s' % e)
    return redirect(url_for('user', username=username))

@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    cur = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        cur.execute('select * from users where username=%s',
                    (username,))
        user = cur.fetchone()
        
        if user is None:
            flash("User %s could not be found" % username)
            return redirect(url_for('index'))
        if user == g.current_user:
            flash('You can\'t unfollow yourself!')
            return redirect(url_for('user', username=username))
        cur.execute('select * from followers where follower=%s and following=%s;',
                    (g.current_user["id"], user["id"]))
        
        u = cur.fetchone()
        print u
        if u is None:
            flash('Already not following ' + username + '.')
            return redirect(url_for('user', username=username))
        cur.execute('delete from followers where follower=%s and following=%s;',
                    (g.current_user["id"], user["id"]))
        g.db.commit()
        cur.close()
        flash('You are no longer following ' + username + '!')
    except psycopg2.DatabaseError, e:
        flash('Error %s' % e)
    return redirect(url_for('user', username=username))


def is_following(id1, id2):
    cur = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('select * from followers where follower=%s and following=%s;',(id1,id2))
    u = cur.fetchone()
    cur.close()
    if u is None:
        return False
    else:
        return True
    


if __name__ == '__main__':
    app.run()
