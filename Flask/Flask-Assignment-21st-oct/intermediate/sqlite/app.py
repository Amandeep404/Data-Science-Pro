from flask import Flask, render_template, request, redirect, url_for
import sqlite3 as sql
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

# Sql logic
DATABASE_LOCATION = 'Flask-Assignment-21st-oct/intermediate/sqlite/todos.db'
connection = sql.connect(DATABASE_LOCATION)
connection.execute('CREATE TABLE IF NOT EXISTS todos (id INTEGER PRIMARY KEY AUTOINCREMENT, task TEXT NOT NULL, completed BOOLEAN NOT NULL)')
connection.close()

@app.route('/')
def home():
    conn = sql.connect(DATABASE_LOCATION)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM todos')
    todos = cursor.fetchall()
    conn.close()
    return render_template('home.html', todos=todos)   

@app.route('/add', methods=['POST'])
def add():
    task = request.form['task']
    conn = sql.connect(DATABASE_LOCATION)
    conn.execute('INSERT INTO todos(task, completed) VALUES (?, ?)', (task, False))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))
    
@app.route('/update/<todo_id>', methods = ['GET', 'POST'])
def update(todo_id):
    conn = sql.connect(DATABASE_LOCATION)
    c = conn.cursor()
    c.execute('SELECT * FROM todos WHERE id=?', (todo_id,))
    data = c.fetchone()
    
    if request.method == 'POST':
        task = request.form['task']
        conn.execute('UPDATE todos SET task = ? WHERE id = ?', (task, todo_id))
        conn.commit()
        conn.close()
        return redirect(url_for('home'))
    else:
        return render_template('update.html', data=data)

@app.route('/delete/<todo_id>')
def delete(todo_id):
    conn = sql.connect(DATABASE_LOCATION)
    conn.execute('DELETE FROM todos WHERE id = ?', (todo_id))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))
    


if __name__== '__main__':
    app.run(debug=True)