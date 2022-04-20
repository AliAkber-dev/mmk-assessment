from flask_restful import Resource
from flask_apispec.views import MethodResource
from server import redis_client
from server.routes import auth, param_validation
from flask import request, make_response
from wtforms.validators import DataRequired
from flask_inputs import Inputs
from server.models import PhoneNumber

class InboundInputs(Inputs):
    json = {
        'from': [DataRequired(message="from is missing"),param_validation],
        'to': [param_validation],
        'text': [param_validation]
    }

class InboundAPI(MethodResource,Resource):
    @auth.login_required
    def post(self):
        current_account_id = auth.current_user().id
        request_obj = request.get_json()
        #req = InboundForm(data=request_obj)
        req = InboundInputs(request)
        response = {}
        status_code = 200
        response["message"] = ""
        response["error"] = ""
        try:
            if(req.validate()):
                check_to = PhoneNumber.query.filter_by(account_id=current_account_id, number=request_obj["to"]).first()
                if(check_to):
                    if(request_obj["text"].rstrip()=="STOP"):
                        hash = f"STOP_{request_obj['from']}:{request_obj['to']}"
                        redis_client.hset(hash,request_obj["from"],request_obj["to"])
                        redis_client.expire(hash,4*60*60)
                        value = redis_client.hget(hash,request_obj["from"])
                        response["message"] = "inbound sms ok"
                else:
                    status_code = 404
                    response["error"] = "to parameter not found"
            else:
                response["error"] = (req.errors)
                status_code = 400
        except:
            status_code = 500
            response["message"]=""
            response["error"] = "unknown failure"
        finally:
            return make_response(response,status_code)
