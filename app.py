from flask import Flask, request,jsonify, render_template,make_response
from flask_inputs import Inputs
from flask_inputs.validators import JsonSchema
from flask_httpauth import HTTPBasicAuth
schema_ib = {
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
   },
   'required': ['from']
}
schema_ob = {

}
app = Flask(__name__)
auth = HTTPBasicAuth()
USER_DATA= {
    "arz1":"qwerty_1"
}
@auth.verify_password
def verify_password(username, password):
    if (not (username and password)):
        return False
    return USER_DATA.get(username) == password

class InboundInputs(Inputs):
   json = [JsonSchema(schema=schema_ib)]


@app.route("/inbound/sms",methods=["GET","POST"])
@auth.login_required
def inbound_sms():
    req_obj = request
    req = InboundInputs(req_obj)
    response = {}
    status_code = 200
    if(req.validate()):
        response["msg"] = "True"
        response["status_code"] = str(status_code)
    else:
        response["msg"] = str(req.errors)
        status_code = 400
        response["status_code"] = str(status_code) 
    return make_response(response,status_code)

@app.route("/outbound/sms",methods=["POST"])
def outbound_sms():
    return make_response({"msg":"hello_world"},200)

if __name__ == "__main__":
    app.run(host="127.0.0.1",port=8080, debug=True)