from flask import Flask, render_template, url_for, session, redirect, request
from flask_session import Session
from datetime import timedelta

app = Flask(__name__)

app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(minutes=5) # This is to make the session permanent for 5 minutes


@app.route('/')
def home():
    return "<h1>This is the Home Page</h1>"

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method=='POST':
        session.permanent = True # session will last for 5 minutes and if it is false then it will be deleted when the browser is closed
        user = request.form['username']
        session['current_user']= user
        return redirect(url_for('user'))
    else:
        if "current_user" in session:
            return redirect(url_for('user'))
        return render_template('login.html')
    
@app.route('/user')
def user():
    if 'current_user' in session:
        user = session['current_user']
        return f'<h2>This is your Username -> {user}</h2>'
    else:
        return redirect(url_for('login'))
    
@app.route('/logout')
def logout():
    session.pop('current_user', None)
    return redirect(url_for('login'))


if __name__=='__main__':
    app.run(debug=True)