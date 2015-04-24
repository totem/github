import json
from flask import Response, jsonify
from conf.appconfig import MIME_JSON


def build_response(output, status=200, mimetype=MIME_JSON, headers={}):
    if isinstance(output, list):
        resp = Response(json.dumps(output))
    elif isinstance(output, str):
        resp = jsonify({"status": output})
    else:
        resp = jsonify(output)
    resp.mimetype = mimetype
    return resp, status, headers
