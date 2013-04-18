from functools import wraps
from flask import jsonify
from flask import request, Response
import settings


def check_auth(username, password):
    import settings
    return username == settings.BASIC_USERNAME and password == settings.BASIC_PASSWORD

def authenticate():
    message = {'message': "Authenticate."}
    resp = jsonify(message)

    resp.status_code = 401
    resp.headers['WWW-Authenticate'] = 'Basic realm="Secure"'

    return resp

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth:
            return authenticate()

        elif not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    return decorated



def requires_apitoken(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            request.headers.get('apitoken')

            if request.headers.get('apitoken') == "1234":
                return f(*args, **kwargs)
            else:
                message = {'message': "Authenticate."}
                resp = jsonify(message)
                resp.status_code = 401
                return resp
        except Exception, e:
            indigo.server.log(str(e))

    return decorated