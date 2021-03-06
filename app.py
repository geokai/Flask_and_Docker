"""Simple Flask web app implementation"""

from functools import wraps
import sqlite3
from flask import Flask, flash, g, redirect, render_template, request, \
        session, url_for


# create the application object:
app = Flask(__name__)

app.secret_key = "my precious"
app.database = "sample.db"


# login required decorator:
def login_required(function):
    """this decorator ensures only logged in users can access"""
    @wraps(function)
    def wrap(*args, **kwargs):
        """wrapper decorator"""
        if 'logged_in' in session:
            return function(*args, **kwargs)
        flash('You need to login first.')
        return redirect(url_for('login'))
    return wrap


# use decorators to link the function to a url:
@app.route('/')
def home():
    """calls the web site home page"""
    return render_template("index.html")


@app.route('/welcome')
@login_required
def welcome():
    """calls the web site welcome page"""
    g.db = connect_db()
    cur = g.db.execute('select * from posts')
    posts = [dict(title=row[0], description=row[1]) for row in cur.fetchall()]
    g.db.close()
    return render_template("welcome.html", posts=posts)


#  route for handling the login page logic:
@app.route('/login', methods=['GET', 'POST'])
def login():
    """calls the web site login page"""
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or \
                request.form['password'] != 'admin':
            error = 'Invalid credentials. Please try again.'
        else:
            session['logged_in'] = True
            flash('You were successfully logged in!')
            return redirect(url_for('welcome'))
    return render_template('login.html', error=error)


@app.route('/logout')
@login_required
def logout():
    """runs the logout logic"""
    session.pop('logged_in', None)
    flash('You were successfully logged out!')
    return redirect(url_for('login'))


def connect_db():
    """create a databse object"""
    return sqlite3.connect(app.database)


# start the sever with the 'run()' method:
if __name__ == '__main__':
    app.run(debug=True)
