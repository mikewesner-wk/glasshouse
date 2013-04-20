from flask import request, render_template, flash, url_for, redirect
from application import app
import httplib2
from application.decorators import login_required, admin_required

from oauth2client.appengine import StorageByKeyName, CredentialsNDBModel
from oauth2client.client import OAuth2WebServerFlow
from application import secret_keys
from google.appengine.api import users

from application import call

@app.route('/signup')
@login_required
def signup():
    authorize_url = call.flow.step1_get_authorize_url()
    return redirect(authorize_url)


@app.route('/oauth2callback')
def oauth2callback():
    call.flow = OAuth2WebServerFlow(
            client_id=secret_keys.G_API_CLIENT_ID,
            client_secret=secret_keys.G_API_CLIENT_SECRET,
            redirect_uri='https://xglasshouse.appspot.com/oauth2callback',
            scope='https://www.googleapis.com/auth/userinfo.profile',
            user_agent='my-sample/1.0')

    user = users.get_current_user()

    if request.args.get('code'):

        credentials = call.flow.step2_exchange(request.args.get('code'))
        storage = StorageByKeyName(
            CredentialsNDBModel, user.user_id(), 'credentials'
        )
        storage.put(credentials)

        http = httplib2.Http()
        http = credentials.authorize(http)

        return "credentials successfully stored!"

    elif request.args.get('error'):
        return "User denied the request for credentials"

@app.route('/testoa1')
@login_required
def testoa1():
    user = users.get_current_user()

    resp = call.get('https://www.googleapis.com/oauth2/v2/userinfo', userid=user.user_id())

    return resp.text


