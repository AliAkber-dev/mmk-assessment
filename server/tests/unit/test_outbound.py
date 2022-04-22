
import pytest
from server.routes.outbound import OutboundInputs
import json 
from flask import Request
from server.models import Account, PhoneNumber
from server import redis_client
def test_1_outbound_api(flask_app):
    #check for method not allowed request (405)
    url = '/outbound/sms'
    response = flask_app.get(url)
    print(response)
    assert response.status_code == 405

@pytest.mark.parametrize(
    ('auth_credentials'),
    (
        (
            {
                "username":"",
                "password":""
            }
        ),
        (
            {
                "username":"azr1",
                "password":"20S0KPNOIM"
            }
        )
    )
)
def test_2_outbound_api(flask_app,auth_credentials):
    url = '/outbound/sms'
    response = flask_app.post(url,auth=(auth_credentials["username"],auth_credentials["password"]))
    auth_check = auth_credentials["username"] and auth_credentials["password"]
    if(auth_check):
        assert response.status_code != 403 # status code is not 403, hence user was authorized
    else:
        assert response.status_code == 403 # status code is 403, hence user was not authorized


auth_credentials = {
    "username":"azr1",
    "password":"20S0KPNOIM"
}
req = [
    {
    "data":{
        "to":"",
        "from":"",
        "text":""
    }
    },
    {
    "data":{
        "to":"1231231",
        "from":""
    },
    },
    {
    "data":{
        "to":"4924195509198",
        "from":"123126",
        "text":"1"
    },
    },
    {
    "data":{
        "to":"49241955091",
        "from":"4924195509198",
        "text":"1"
    },
    }  
]
@pytest.mark.parametrize('req',req)
def test_3_outbound_api(flask_app, req):
    url = '/outbound/sms'
    headers = {'Content-type': 'application/json'}
    response = flask_app.post(url, auth=(auth_credentials["username"], auth_credentials["password"]), json=req["data"], headers = headers)
    fields_check = ["to","from","text"] == list(req["data"].keys())
    if(not fields_check):
        assert response.status_code == 400
    if(fields_check):
        type_check = type(req["data"]["to"])== str and type(req["data"]["from"])==str and type(req["data"]["text"])==str 
        len_check = (len(req["data"]["to"])<=16 and len(req["data"]["to"])>=6) and (len(req["data"]["from"])<=16 and len(req["data"]["from"])>=6) and (len(req["data"]["text"])>0 and len(req["data"]["text"])<121)
        if(type_check and len_check):
            account_id = Account.query.filter_by(username=auth_credentials["username"],auth_id=auth_credentials["password"]).first().id
            phone_number_record =  PhoneNumber.query.filter_by(account_id=account_id, number=req["data"]["from"]).first()
            if(phone_number_record):
                assert response.status_code == 200
            else:
                assert response.status_code == 404
        else:
            assert response.status_code == 400

#Test if limiting API works fine
req = [
    {
    "data":{
        "to":"123126",
        "from":"4924195509196",
        "text":"HI"
        }
    }
]
@pytest.mark.parametrize('req',req)
def test_4_outbound_api(flask_app,req):
    url_outbound = '/outbound/sms'
    headers = {'Content-type': 'application/json'}
    response_outbound = flask_app.post(url_outbound,auth=(auth_credentials["username"],auth_credentials["password"]),json=req["data"],headers = headers)  
    assert response_outbound.status_code == 200
    for _ in range(0,50):
        response_outbound = flask_app.post(url_outbound,auth=(auth_credentials["username"],auth_credentials["password"]),json=req["data"],headers = headers)
    assert response_outbound.status_code == 429
    hash_limit = f"LIMIT_{req['data']['from']}"
    redis_client.delete(hash_limit)
