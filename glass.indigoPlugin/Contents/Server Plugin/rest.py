from flask import Flask, url_for, Response, json, jsonify
app = Flask(__name__)
import indigo
from basicauth import requires_auth

@app.route('/logs')
def api_root():
    return 'Welcome'

@app.route('/devices', methods = ['GET'])
@requires_auth
def api_devices():
    data = dict([(d.address, d.name) for d in indigo.devices])
    resp = jsonify(data)
    resp.status_code = 200
    return resp

@app.route('/devices/<deviceid>')
def api_article(deviceid):
    return 'Device ' + deviceid

