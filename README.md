# psychoflask
Flask blog with minimal extensions and full text search.

Attempt at making a flask app without an ORM. Login/sessions stuff is crappy (didn't seem possible to use Flask-Login), but implements a basic "microblog" using only one or two flask extensions. Requires Flask-WTF for forms, which you could get around without, and Flask-Script, which you definitely don't need. Might be a bit buggy, but I'll try to remove them when they show up. I use the psycopg2 postgres adaptor a lot and would appreciate sql tips! I used postgres/psycopg2 for pretty much everything including a basic full text search. I also tried to make a scrolling news feed that uses some ajax stuff to request more news items when you scroll to the bottom of the page (like facebooks newsfeed).

Basically the app is in app.py, but you run ```python manage.py runserver``` to start the app. To create the initial database run the following from within the root directory of the repo:
```
python manage.py initdb
```

This should work, but if it doesn't you can try creating the db using psql in the following way:
```
create database flaskr;
```

which creates the database (I named it flaskr). Then run the following to add the tables/triggers (once you've connected to the new db):
```
\i createdb.sql
```
