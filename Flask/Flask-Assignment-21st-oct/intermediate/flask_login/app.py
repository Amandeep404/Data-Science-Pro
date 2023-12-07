from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
import bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.secret_key = 'secret_key'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), unique = True, nullable = False)
    password = db.Column(db.String(1000), nullable = False)
    
    def __init__(self, name,email, password):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
    def check_pswd(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

# important to create the database before running the app
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dashboard')
def dashboard():
    if session['user_name']:
        user = User.query.filter_by(email = session['email']).first()
        return render_template('dashboard.html', user = user)    
    return redirect(url_for('login'))

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
        new_user = User(name, email, password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful !!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'] 
        
        user = User.query.filter_by(email = email).first()
        
        if user and user.check_pswd(password):
            session['user_name'] = user.name
            session['email'] = user.email
            flash('Login successful!', 'success') 
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger') 
            return render_template('login.html', error = 'Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('login'))

if __name__=='__main__':
    app.run(debug=True)