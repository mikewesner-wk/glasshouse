from requests import Request, Session, request, api
from oauth2client.appengine import StorageByKeyName, CredentialsNDBModel
from oauth2client.client import OAuth2WebServerFlow
from google.appengine.api import users
import httplib2
from application import secret_keys

flow = OAuth2WebServerFlow(
    client_id=secret_keys.G_API_CLIENT_ID,
    client_secret=secret_keys.G_API_CLIENT_SECRET,
    redirect_uri='https://xglasshouse.appspot.com/oauth2callback',
    scope='https://www.googleapis.com/auth/userinfo.profile',
    user_agent='my-sample/1.0')

def _get_creds(userid):
    user = users.get_current_user()
    storage = StorageByKeyName(
        CredentialsNDBModel, userid, 'credentials'
    )
    credentials = storage.get()
    return credentials

def _setup_oauth2_headers(credentials, headers):
    http = httplib2.Http()
    http = credentials.authorize(http)
    headers['Authorization'] = "Bearer %s" % (http.request.credentials.access_token)
    return headers


def _refresh_oauth2_token(credentials, userid):
    http = httplib2.Http()
    credentials.refresh(http)
    storage = StorageByKeyName(CredentialsNDBModel, userid, 'credentials')
    storage.put(credentials)
    return credentials

def get(url, **kwargs):
    return req(api.get, url, **kwargs)

def post(url, **kwargs):
    return req(api.post, url, **kwargs)



def req(apifunc, url, **kwargs):
    """
    """
    userid = kwargs.get('userid', None)
    headers = kwargs.get('headers', {})
    if userid:
        kwargs.pop('userid')
        credentials = _get_creds(userid)
        if credentials:
            headers = _setup_oauth2_headers(credentials, headers)

    kwargs['headers'] = headers
    resp = apifunc(url, **kwargs)

    if credentials and resp.status_code == 401:
        credentials = _refresh_oauth2_token(credentials)
        headers = _setup_oauth2_headers(credentials, headers)
        kwargs['headers'] = headers
        resp = apifunc(url, **kwargs)

    return resp