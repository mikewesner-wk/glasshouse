import logging

from requests import api
from oauth2client.appengine import StorageByKeyName, CredentialsNDBModel
from oauth2client.client import OAuth2WebServerFlow
import httplib2
from application import secret_keys

GLASS_TIMELINE_API = 'https://www.googleapis.com/auth/glass.timeline'
USER_INFO_API = 'https://www.googleapis.com/auth/userinfo.profile'
scopes = [USER_INFO_API, GLASS_TIMELINE_API]

flow = OAuth2WebServerFlow(
    client_id=secret_keys.G_API_CLIENT_ID,
    client_secret=secret_keys.G_API_CLIENT_SECRET,
    redirect_uri=secret_keys.G_API_REDIRECT,
    scope=scopes,
    user_agent='my-sample/1.0')


def _get_creds(userid):
    """
    We store the credentials by google userid from the users api.
    """
    storage = StorageByKeyName(
        CredentialsNDBModel, userid, 'credentials'
    )
    credentials = storage.get()
    return credentials

def _delete_creds(userid):
    storage = StorageByKeyName(
        CredentialsNDBModel, userid, 'credentials'
    )
    if storage.get():
        credentials = storage.locked_delete()
        return True

    return False

def _setup_oauth2_headers(credentials, headers):
    """
        oauth2client library has OAuth2Credentials class which modifies
        httplib2.request and handles all the refresh magic for us and headers.
        I decided to just leverage that existing code to do all the work.
        We just steal the resulting access token and then use the requests
        library instead.
    """
    http = httplib2.Http()
    http = credentials.authorize(http)
    headers['Authorization'] = "OAuth %s" \
        % (http.request.credentials.access_token)
    return headers


def _refresh_oauth2_token(credentials, userid):
    """
    This updates the token via the OAuth2Credentials code and
    modifies the httplib2.Http.request stuff.  We store the updated
    credentials for later.
    """
    from oauth2client.client import AccessTokenRefreshError

    http = httplib2.Http()
    http = credentials.authorize(http)
    storage = StorageByKeyName(CredentialsNDBModel, userid, 'credentials')
    try:
        credentials.refresh(http)
    except AccessTokenRefreshError:
        logging.info("AccessTokenRefreshError: lets delete the creds.")
        storage.delete()
        return
    storage.put(credentials)
    return credentials


#
# These are all passthroughs to requests.api.*
def get(url, **kwargs):
    return req(api.get, url, **kwargs)


def post(url, **kwargs):
    return req(api.post, url, **kwargs)


def put(url, **kwargs):
    return req(api.put, url, **kwargs)


def delete(url, **kwargs):
    return req(api.delete, url, **kwargs)


def head(url, **kwargs):
    return req(api.head, url, **kwargs)


def options(url, **kwargs):
    return req(api.options, url, **kwargs)


def req(apifunc, url, **kwargs):
    """
    This is just a passthrough to requests library, but it
    wraps it to:
    1. add the oauth token header based on user id
    2. catches response code 401, updates the token, and calls again
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

    if userid and credentials and resp.status_code == 401:
        credentials = _refresh_oauth2_token(credentials, userid)
        headers = _setup_oauth2_headers(credentials, headers)
        kwargs['headers'] = headers
        resp = apifunc(url, **kwargs)

    return resp
