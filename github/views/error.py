import flask
import traceback
from flask import request
from datetime import datetime


def as_flask_error(error=None, message=None, details=None, traceback=None,
                   status=500, code="INTERNAL", timestamp=None):
    return flask.jsonify({
        "path": request.path,
        "url": request.url,
        "method": request.method,
        "message": message,
        "details": details,
        "traceback": traceback,
        "status": status,
        "code": code,
        "timestamp": timestamp or datetime.utcnow()
    }, status=status), status


class HooksFailed(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, details=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status = status_code
        self.details = details

    def to_dict(self):
        rv = {
            "message": self.message,
            "details": self.details
        }
        return rv


def register(app, **kwargs):
    @app.errorhandler(404)
    def page_not_found(error):
        return as_flask_error(error, **{
            "message": "The given resource:%s is not found on server"
                       % request.path,
            "code": "NOT_FOUND",
            "status": 404
        })

    @app.errorhandler(HooksFailed)
    def hook_error(error):
        return as_flask_error(error, **{
            "details": error.details,
            "message": error.message,
            "code": "HOOK_ERROR",
            "status": error.status
        })

    @app.errorhandler(Exception)
    @app.errorhandler(500)
    def internal(error):
        trace = traceback.format_exc()
        try:
            details = error.to_dict()
        except AttributeError:
            details = None
        return as_flask_error(error, **{
            "details": details,
            "traceback": trace,
            "status": 500
        })
