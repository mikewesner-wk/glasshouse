from flask import Flask, url_for, Response, json, jsonify
app = Flask(__name__)
import indigo
from basicauth import requires_auth

@app.route('/logs')
@requires_auth
def api_logs():
    resp = jsonify(indigo.server.getEventLogList().split('\n'))
    resp.status_code = 200
    return resp

@app.route('/devices', methods = ['GET'])
@requires_auth
def api_devices():
    data = dict([(d.address, d.name) for d in indigo.devices])
    resp = jsonify(data)
    resp.status_code = 200
    return resp

@app.route('/devices/<deviceid>')
def api_device_by_id(deviceid):
    pass

