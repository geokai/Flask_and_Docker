"""Simple Flask web site implementation"""


from flask import Flask, render_template, redirect, url_for, request


# create the application object:
app = Flask(__name__)

# use decorators to link the function to a url:
@app.route('/')
def home():
    # return "Hello, world!"
    return render_template("index.html")

@app.route('/welcome')
def welcome():
    return render_template("welcome.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid credentials. Please try again.'
        else:
            return redirect(url_for('welcome'))
    return render_template('login.html', error=error)

# start the sever with the 'run()' method:
if __name__ == '__main__':
    app.run(debug=True)
