from flask import Flask, render_template, url_for
app=Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/username/<name>')
def username(name):
    return render_template('user_profile.html', username=name)


if __name__ == '__main__':
    app.run(debug=True)