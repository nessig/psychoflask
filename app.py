from flask import Flask, render_template, g, redirect, url_for, flash, session, request
# import db
import psycopg2
import psycopg2.extras
from contextlib import closing
from datetime import datetime
from forms import LoginForm, RegisterForm, EditForm, PostForm, SearchForm, CommentForm
from functools import wraps

### TODO: Add news feed scrolling and add comments

# configuration
DATABASE = 'flaskr'
DEBUG = True
SECRET_KEY = '\x03BSx\x8aoM0E\xb7 \xa5\xb3+\x9e\x83\x03A.\xa3i\xa1`\xf3'
USERNAME = 'nessig'
PASSWORD = '123'

DSN = "dbname=%s user=%s password=%s" % (DATABASE, USERNAME, PASSWORD)

app = Flask(__name__,static_url_path='')
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
        with app.open_resource('createdb.sql', mode='r') as f:
            cursor.execute(f.read())
        conn.commit()


# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'user_id' in session and session["user_id"] is not None:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login', next=request.url))
    return wrap


@app.before_request
def before_request():
    g.db = connect_db()
    g.search_form = SearchForm()
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
    if g.current_user is not None:
        cur.execute(getFollowingPostsSQL, (g.current_user['id'],))
        # users = cur.fetchall()
    
        # user_ids = [user["id"] for user in users]
        # cur.execute("select * from posts where author_id=ANY(%s)", (user_ids,))
        posts = cur.fetchall()
        # print posts
        cur.close()
        return render_template("index.html",
                           posts=posts)
    else:
        return render_template("welcome.html")


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
@app.route('/user/<username>/post/<postid>', methods=['GET', 'POST'])
def user(username, postid=None):
    form = PostForm(prefix="form1")
    formComment = CommentForm(prefix="form2")
    cur = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        cur.execute('select * from users where username=%s',
                    (username,))
        user = cur.fetchone()
        if user is not None:
            if postid is not None:
                
                if formComment.validate_on_submit():
                    commenter_id = g.current_user["id"]
                    comment_date = datetime.utcnow()
                    comment_text = formComment.comment.data
                    cur.execute('select id from posts where author_id=%s and title=%s;',
                                (user["id"], postid))
                    post_id = cur.fetchall()[0][0]
                    formComment.comment.data = None
                    cur.execute('insert into comments (comment_date,comment_text,commenter_id,post_id) values (%s,%s,%s,%s);',
                                (comment_date,comment_text,commenter_id,post_id))
                    g.db.commit()
                    
                    return redirect(url_for('user', username=user["username"], postid=postid))
                cur.execute('select * from posts where author_id=%s and title=%s;',
                            (user["id"], postid))
                post = cur.fetchone()
                commentsSQL = """
                select comment_date,username,comment_text
                from users
                inner join comments
                on (users.id=commenter_id)
                where post_id=%s;
                """
                # cur.execute('select * from comments where post_id=%s order by comment_date desc;',
                #             (post["id"],))
                cur.execute(commentsSQL, (post["id"],))
                comments = cur.fetchall()
                cur.close()
                return render_template('postpage.html',
                                       formComment=formComment,
                                       user=user,
                                       post=post,
                                       comments=comments)
            
            if form.validate_on_submit():
                title = form.title.data
                body = form.body.data
                author_id = user["id"]
                cur.execute('insert into posts (title,body,author_id,pub_date) values (%s,%s,%s,%s)',
                            (title, body, author_id,datetime.utcnow()))
                g.db.commit()
                return redirect(url_for('user', username=user['username']))
            
            isfollowing = is_following(g.current_user["id"], user["id"])
            cur.execute('select * from posts where author_id=%s order by pub_date desc',
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
    

@app.route('/search', methods=['POST'])
@login_required
def search():
    if not g.search_form.validate_on_submit():
        return redirect(url_for('index'))
    return redirect(url_for('search_results', query=g.search_form.search.data))


searchquery = """
select * from posts
where to_tsvector(title) @@ plainto_tsquery(%s)
or to_tsvector(body) @@ plainto_tsquery(%s);
"""

    # searchquery = """
# select post.* from posts post,
# plainto_tsquery(%s) q
# where q @@ (to_tsvector(title) ||  to_tsvector(body));
# """


# searchquery = """
# select post.* from posts post,
# plainto_tsquery(%s) q
# where q @@ (to_tsvector(title) ||  to_tsvector(body));
# """


# searchquery = """
# SELECT ts_headline(title, q) as title_headline,
# ts_headline(body,q) as body_headline FROM(
# select title,body,tsv,q
# from posts, plainto_tsquery(%s) as q
# WHERE (tsv @@ q)
# ) as t1 ORDER BY ts_rank_cd(t1.tsv, plainto_tsquery(%s)) DESC LIMIT 5;
# """

def userFromAuthorID(id):
    cur = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = "select * from users where id=%s"
    cur.execute(query, (id,))
    user = cur.fetchone()
    return user


@app.route('/search_results/<query>')
@login_required
def search_results(query):
    cur = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    searchquery = """
    select username,
    title_headline,
    body_headline,
    pub_date
    from users
    inner join (SELECT author_id,pub_date,
    ts_headline(title, q) as title_headline,
    ts_headline(body,q,'MaxWords=6,MinWords=3,
    MaxFragments=3, FragmentDelimiter=" ... "')
    as body_headline
    FROM(
    select author_id,title,body,tsv,q,pub_date
    from posts,plainto_tsquery(%s) as q
    WHERE (tsv @@ q)
    ) as t1 ORDER BY
    ts_rank_cd(t1.tsv, plainto_tsquery(%s)) DESC LIMIT 5)
    as foo
    on (users.id=author_id);
    """
    cur.execute(searchquery, (query, query))
    results = cur.fetchall()
    # print results
    cur.close()
    return render_template('searchResults.html',
                           results=results,
                           query=query)


# if __name__ == '__main__':
#     app.run()
