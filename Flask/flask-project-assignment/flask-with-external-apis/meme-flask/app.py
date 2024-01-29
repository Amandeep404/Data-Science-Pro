from flask import Flask, render_template, session
import requests

app = Flask(__name__)

API_URL = "https://api.imgflip.com/get_memes"
app.secret_key = "super secret key"

def get_random_meme(index):
    request = requests.get(API_URL)
    if request.status_code == 200:
        memes = request.json()['data']['memes']
        return memes[index]

@app.route("/")
def home():
    current_index = session.get('current_index', 0)

    meme = get_random_meme(current_index)

    meme_title = meme['name']
    meme_image_url = meme['url']

    return render_template("index.html", meme_title=meme_title, meme_image_url=meme_image_url)

@app.route("/previous")
def previous_meme():
    current_index = session.get('current_index', 0)

    current_index = (current_index - 1) % len(requests.get(API_URL).json()['data']['memes'])

    session['current_index'] = current_index

    return home()

@app.route("/next")
def next_meme():
    current_index = session.get('current_index', 0)

    current_index = (current_index + 1) % len(requests.get(API_URL).json()['data']['memes'])

    session['current_index'] = current_index

    return home()

if __name__ == "__main__":
    app.run(debug=True)
