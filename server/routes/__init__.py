from flask_restful import Resource
from flask_apispec.views import MethodResource
from server import db
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()
from flask_inputs import Inputs
from flask_inputs.validators import JsonSchema

schema = {
   "type": "object",
   "properties": {
       "from": {
           "type": "string",
           "minLength":6,
           "maxLength":16
       },
       "to":{
           "type":"string",
           "minLength":6,
           "maxLength":16
       },
       "text":{
           "type":"string",
           "minLength":1,
           "maxLength":120
       }
   }
}

@auth.verify_password
def verify_password(username, password):
    if (not (username and password)):
        return False
    return USER_DATA.get(username) == password


class InboundInputs(Inputs):
    schema["required"] = ["from"]
    json = [JsonSchema(schema=schema)]

class OutboundInputs(Inputs):
    schema["required"] = ["from","to"]
    json = [JsonSchema(schema=schema)]

class InboundAPI(MethodResource,Resource):
    @auth.login_required
    def post():
        request_obj = request.get_json()
        req = InboundInputs(request)
        response = {}
        status_code = 200
        if(req.validate()):
            response["message"] = "True"
            response["status_code"] = str(status_code)
            if(request_obj["text"].rstrip()=="STOP"):
                hash = f"STOP_{request_obj['from']}:{request_obj['to']}"
                redis_client.hset(hash,request_obj["from"],request_obj["to"])
                redis_client.expire(hash,4*60*60)
                value = redis_client.hget(hash,request_obj["from"])
                print(value)
        else:
            response["message"] = str(req.errors)
            status_code = 400
            response["status_code"] = str(status_code) 
        return make_response(response,status_code)

    