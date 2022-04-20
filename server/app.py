from flask import Flask, request,jsonify, render_template,make_response
from flask_inputs import Inputs
from flask_inputs.validators import JsonSchema
from flask_httpauth import HTTPBasicAuth
from flask_redis import FlaskRedis
from flask_sqlalchemy import SQLAlchemy
from server import app,api
from server.routes.inbound import InboundAPI
from server.routes.outbound import OutboundAPI
#, OutboundAPI
# schema = {
#    "type": "object",
#    "properties": {
#        "from": {
#            "type": "string",
#            "minLength":6,
#            "maxLength":16
#        },
#        "to":{
#            "type":"string",
#            "minLength":6,
#            "maxLength":16
#        },
#        "text":{
#            "type":"string",
#            "minLength":1,
#            "maxLength":120
#        }
#    }
# }
# auth = HTTPBasicAuth()
# USER_DATA= {
#     "arz1":"qwerty_1"
# }
# @auth.verify_password
# def verify_password(username, password):
#     if (not (username and password)):
#         return False
#     return USER_DATA.get(username) == password

# class InboundInputs(Inputs):
#     schema["required"] = ["from"]
#     json = [JsonSchema(schema=schema)]

# class OutboundInputs(Inputs):
#     schema["required"] = ["from","to"]
#     json = [JsonSchema(schema=schema)]


# @app.route("/inbound/sms",methods=["POST"])
# @auth.login_required
# def inbound_sms():
#     request_obj = request.get_json()
#     req = InboundInputs(request)
#     response = {}
#     status_code = 200
#     if(req.validate()):
#         response["message"] = "True"
#         response["status_code"] = str(status_code)
#         if(request_obj["text"].rstrip()=="STOP"):
#             hash = f"STOP_{request_obj['from']}:{request_obj['to']}"
#             redis_client.hset(hash,request_obj["from"],request_obj["to"])
#             redis_client.expire(hash,4*60*60)
#             value = redis_client.hget(hash,request_obj["from"])
#             print(value)
#     else:
#         response["message"] = str(req.errors)
#         status_code = 400
#         response["status_code"] = str(status_code) 
#     return make_response(response,status_code)

api.add_resource(InboundAPI, '/inbound/sms')
api.add_resource(OutboundAPI,'/outbound/sms')
# @app.route("/outbound/sms",methods=["POST"])
# @auth.login_required
# def outbound_sms():
#     request_obj = request.get_json()
#     req = OutboundInputs(request)
#     response = {}
#     status_code = 200
#     if(req.validate()):
#         response["message"] = "True"
#         response["status_code"] = str(status_code)
#         hash = f"STOP_{request_obj['to']}:{request_obj['from']}"
#         cache_entry = redis_client.hget(hash,request_obj["to"])
#         if(cache_entry):
#             response["message"] = ""
#             response["error"] =  f"sms from {request_obj['from']} to {request_obj['to']} blocked by STOP request"
#         hash = f"LIMIT_{request_obj['from']}"
#         if(redis_client.hsetnx(hash,request_obj["from"],50)):
#             redis_client.expire(hash, 24*60*60)
#             print("here")
#         current_limit_value = redis_client.hget(hash,request_obj["from"])
#         if(current_limit_value and int(current_limit_value)>0): 
#             print("previous_count",str(current_limit_value))
#             updated_limit_value = int(current_limit_value) - 1
#             redis_client.hset(hash,request_obj["from"],updated_limit_value)
#         else:
#             response["message"] = ""
#             response["errors"] = f"limit reached for from {request_obj['from']}"
#             status_code = 429
#     else:
#         response["msg"] = str(req.errors)
#         status_code = 400
#         response["status_code"] = str(status_code) 
#     return make_response(response,status_code)

if __name__ == "__main__":
    app.run(host="127.0.0.1",port=8080, debug=True)