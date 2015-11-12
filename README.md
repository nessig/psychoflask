# psychoflask
Flask blog with minimal extensions.

Attempt at making a flask app without an ORM. Login/sessions stuff is crappy (didn't seem possible to use Flask-Login), but implements a basic "microblog" using only one or two flask extensions. Requires Flask-WTF for forms, which you could get around without, and Flask-Script, which you definitely don't need. Might be a bit buggy, but I'll try to remove them when they show up. I use the psycopg2 postgres adaptor a lot and would appreciate sql tips! I used postgres/psycopg2 for pretty much everything including a basic full text search. I also tried to make a scrolling news feed that uses some ajax stuff to request more news items when you scroll to the bottom of the page (like facebooks newsfeed).
