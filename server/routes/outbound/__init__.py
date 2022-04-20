from flask_restful import Resource
from flask_apispec.views import MethodResource
from server import redis_client
from server.routes import auth, param_validation
from flask import request, make_response
from wtforms.validators import DataRequired
from flask_inputs import Inputs
from server.models import PhoneNumber

class OutboundInputs(Inputs):
    json = {
        'from': [DataRequired(message="from is missing"),param_validation],
        'to': [DataRequired(message="to is missing"), param_validation],
        'text': [param_validation]
    }

class OutboundAPI(MethodResource,Resource):
    @auth.login_required
    def post(self):
        current_account_id = auth.current_user().id
        status_code = 200
        response = {}
        response["message"] = ""
        response["error"] = ""
        request_obj = request.get_json()
        req = OutboundInputs(request)
        try:
            if(req.validate()):
                check_from = PhoneNumber.query.filter_by(account_id=current_account_id, number=request_obj["from"]).first()
                if(check_from):
                    hash = f"STOP_{request_obj['to']}:{request_obj['from']}"
                    cache_entry = redis_client.hget(hash,request_obj["to"])
                    if(cache_entry):
                        response["error"] =  f"sms from {request_obj['from']} to {request_obj['to']} blocked by STOP request"
                    else:
                        hash = f"LIMIT_{request_obj['from']}"
                        if(redis_client.hsetnx(hash,request_obj["from"],50)):
                            redis_client.expire(hash, 24*60*60)
                        current_limit_value = redis_client.hget(hash,request_obj["from"])
                        if(current_limit_value and int(current_limit_value)>0): 
                            #print("previous_count",str(current_limit_value))
                            updated_limit_value = int(current_limit_value) - 1
                            redis_client.hset(hash,request_obj["from"],updated_limit_value)
                            response["message"] = "outbound sms ok"
                        else:
                            response["message"] = ""
                            response["error"] = f"limit reached for from {request_obj['from']}"
                            status_code = 429
                else:
                    status_code = 404
                    response["error"] = "from parameter not found"
            else:
                response["error"] = (req.errors)
                status_code = 400
        except :
            status_code = 500
            response["error"] = "unknown failure" 
        finally:
            return make_response(response,status_code)
