from flask import Flask, request,jsonify, render_template,make_response
from flask_inputs import Inputs
from flask_inputs.validators import JsonSchema
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
from server import app,api
from server.routes.inbound import InboundAPI
from server.routes.outbound import OutboundAPI

api.add_resource(InboundAPI, '/inbound/sms')
api.add_resource(OutboundAPI,'/outbound/sms')

@app.route('/', methods=["GET"])
def helloworld():
    return "Hello World",200

if __name__ == "__main__":
    app.run(host="127.0.0.1",port=8080, debug=True)