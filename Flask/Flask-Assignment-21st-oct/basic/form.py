from flask import Flask, render_template, url_for, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def form_page():
    if request.method=='POST':
        user_name = request.form.get('username')
        user_email = request.form.get('email')
        user_age = request.form.get('age')
        return render_template('result.html', username=user_name, email=user_email, age=user_age)
    else:
        return render_template('form.html')


if __name__=='__main__':
    app.run(debug=True)