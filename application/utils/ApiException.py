# -*- coding: utf-8 -*-

from flask import jsonify

from application import app


# ref : https://flask.palletsprojects.com/en/1.1.x/patterns/apierrors/
class ApiException(Exception):
    status_code = 400

    def __init__(self, payload, section, custom_message=None):
        Exception.__init__(self)

        if payload['code'] is not None:
            self.status_code = payload['code']

        if custom_message is not None:
            self.message = custom_message
        else:
            self.message = payload['message']
        self.section = section
        self.name = payload['name']

    def to_dict(self):

        return {"errors": {
            self.section: {"code": self.name, "name": self.message}
        }}


@app.errorhandler(ApiException)
def handle_api_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
