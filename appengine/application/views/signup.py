from flask import request, render_template, flash, url_for, redirect, Response, json, jsonify
from application import app
import httplib2
from application.decorators import login_required, admin_required

from oauth2client.appengine import StorageByKeyName, CredentialsNDBModel
from oauth2client.client import OAuth2WebServerFlow
from application import secret_keys
from google.appengine.api import users

# my requests library wrapper
from application import call

# https://developers.google.com/api-client-library/python/
from apiclient.discovery import build

@app.route('/signup')
@login_required
def signup():
    authorize_url = call.flow.step1_get_authorize_url()
    return redirect(authorize_url)


@app.route('/oauth2callback')
def oauth2callback():
    user = users.get_current_user()

    if request.args.get('code'):

        credentials = call.flow.step2_exchange(request.args.get('code'))
        storage = StorageByKeyName(
            CredentialsNDBModel, user.user_id(), 'credentials'
        )
        storage.put(credentials)

        http = httplib2.Http()
        http = credentials.authorize(http)
        flash(u'Signin complete.', 'info')
        return redirect('/')

    elif request.args.get('error'):
        return "User denied the request for credentials"


@app.route('/destroy_creds')
def destroy_creds():
    user = users.get_current_user()
    if user:
        if call._delete_creds(user.user_id()):
            flash(u'credentials destroyed.', 'info')
    return redirect('/')


@app.route('/checktoken', methods=['put'])
def checktoken():
    token = request.headers.get('token')


#
# TESTS

@app.route('/testoa1')
@login_required
def testoa1():
    user = users.get_current_user()
    resp = call.get('https://www.googleapis.com/oauth2/v2/userinfo', userid=user.user_id())
    return resp.text

@app.route('/test_userinfo')
@login_required
def test_userinfo():
    user = users.get_current_user()
    credentials = call._get_creds(user.user_id())
    user_info_service = build(
        serviceName='oauth2', version='v2',
        http=credentials.authorize(httplib2.Http()))
    user_info = None
    try:
        user_info = user_info_service.userinfo().get().execute()
    except errors.HttpError, e:
        logging.error('An error occurred: %s', e)

    return str(user_info)


@app.route('/testoa2')
@login_required
def testoa2():
    user = users.get_current_user()
    resp = call.get('https://www.googleapis.com/drive/v2/files', userid=user.user_id())
    return resp.text

