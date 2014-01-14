from flask import Flask, url_for, Response, json, jsonify, request
app = Flask(__name__)
import indigo
from decorators import requires_apitoken, requires_auth
import requests
import db
import settings


#
# Appspot Account Setup Process
@app.route('/token', methods=['PUT'])
def token():
    new_api_token = request.headers.get('token')

    # verify the token with the appengine app
    verify_resp = requests.put(settings.CONTROL_APP + "/checktoken", headers={'token': new_api_token})

    j_resp = verify_resp.json()
    if j_resp['valid']:
        db.set('token', new_api_token)
        resp = jsonify({'success': True})
        resp.status_code = 200
    else:
        resp = jsonify({'success': False})
        resp.status_code = 200

    return resp


@app.route('/dbtest', methods=['GET'])
def dbtest():
    try:
        indigo.server.log("db is " + str(db))
        indigo.server.log(str(dir(db)))
        indigo.server.log(str(type(db.GLOBALSETTINGS)))
        indigo.server.log(str(db.get("mykey")))
        db.put("mykey", "1")
        indigo.server.log(str(db.get("mykey")))
        db.put("mykey", "2")
        indigo.server.log(str(db.get("mykey")))

    except Exception, e:
        return str(e) + "::: " + str(db)

    return '1'

@app.route('/shutdown', methods=['POST'])
@requires_auth
def shutdown():
    from flask import request
    func = request.environ.get('werkzeug.server.shutdown')
    func()
    return 'Shutting Down.'

@app.route('/logs')
@requires_auth
def api_logs():
    try:
        resp = indigo.server.getEventLogList().replace("\n", "<br/>")
        #resp = jsonify({"logs":indigo.server.getEventLogList()})
        #resp.status_code = 200
    except Exception, e:
        indigo.server.log(str(e))
        return None

    return resp

@app.route('/devices', methods = ['GET'])
@requires_apitoken
def api_devices():
    data = dict([(d.address, d.name) for d in indigo.devices])
    resp = jsonify(data)
    resp.status_code = 200
    return resp

@app.route('/devices/<deviceid>')
def api_device_by_id(deviceid):
    pass

