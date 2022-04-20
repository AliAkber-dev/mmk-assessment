from flask_restful import Resource
from flask_apispec.views import MethodResource
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()
from wtforms.validators import ValidationError
from server.models import Account

@auth.verify_password
def verify_password(username, password):
    if (not (username and password)):
        return False
    account = Account.query.filter_by(username=username, auth_id=password).first()
    return account if(account) else False 

def param_validation(form,field):
    type_check = type(field.data) == str
    if(not type_check):
        raise ValidationError(f"{field.name} must be a string")
    if(type_check):
        len_check = False
        upper_limit = 0
        lower_limit = 0
        if(field.name == "text"):
            upper_limit = 120
            lower_limit = 1
        if(field.name == "to" or field.name == "from"):
            upper_limit = 16
            lower_limit = 6
        len_check = len(field.data)<lower_limit or len(field.data)>upper_limit
        if(len_check):
            raise ValidationError(f"{field.name} length must be atleast {lower_limit}  and at most {upper_limit}")
