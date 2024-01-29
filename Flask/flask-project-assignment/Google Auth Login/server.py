from flask import Flask, url_for,session , redirect, render_template, abort
from authlib.integrations.flask_client import OAuth
import json, requests

app = Flask(__name__)

app_config = {
    'OAUTH2_CLIENT_ID':'359090012761-arl7t3sk750kv7pnj7va26919622434r.apps.googleusercontent.com',
    'OAUTH2_CLIENT_SECRET':'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',
    'OAUTH2_META_URL':'https://accounts.google.com/.well-known/openid-configuration',
    'FLASK_SECRET_KEY':'hello',
    'FLASK_PORT':5000
}
app.secret_key = app_config.get('FLASK_SECRET_KEY')


oauth = OAuth(app)
oauth.register(
    'my_flask_app',# this is the name of the app used in the login route /google-login
    client_id=app_config.get('OAUTH2_CLIENT_ID'),
    client_secret=app_config.get('OAUTH2_CLIENT_SECRET'),
    server_metadata_url = app_config.get('OAUTH2_META_URL'),
    # got the scopes from -> https://developers.google.com/identity/protocols/oauth2/scopes
    client_kwargs={
        'scope':'openid profile email  https://www.googleapis.com/auth/user.birthday.read https://www.googleapis.com/auth/user.gender.read '
    }
    )

@app.route('/')
def index():
    return render_template('index.html', 
                           user_session = session.get('user'),
                           pretty_print = json.dumps(session.get('user'), indent=4)
                           )
    
@app.route('/google-signin') 
def googleCallBack():
    #this will take the authorization code from request and use the  client id and client secret and request the google server for id token and access token
    token = oauth.my_flask_app.authorize_access_token() 
    
    # link to the api doc -> https://developers.google.com/people/api/rest/v1/people/get
    # api uri - 'https://people.googleapis.com/v1/{resourceName=people/*}'
    person_data_url = 'https://people.googleapis.com/v1/people/me?personFields=genders,birthdays'
    person_data = requests.get(
        person_data_url,
        headers={
            'Authorization': 'Bearer ' + token.get('access_token')
        }).json
    
    token['person_data'] = person_data()
    session['user'] = token
    return redirect(url_for('index'))


@app.route('/google-login')
def googleLogIn():
    if 'user' in session:
        abort(404)
    return oauth.my_flask_app.authorize_redirect(
        redirect_uri=url_for('googleCallBack', _external=True)
    )

# this route we have mentioned in Authorized redirect URIs in google console  

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

if __name__=='__main__':
    app.run(debug=True, port=app_config.get('FLASK_PORT'))