from flask import Flask, url_for, Response, json, jsonify
app = Flask(__name__)
import indigo
from decorators import requires_apitoken

@app.route('/logs')
@requires_apitoken
def api_logs():
    try:
        #resp = jsonify(indigo.server.getEventLogList().split('\n'))
        resp = jsonify({"logs":indigo.server.getEventLogList()})
        resp.status_code = 200
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

