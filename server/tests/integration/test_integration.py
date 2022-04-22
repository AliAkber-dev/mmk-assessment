import pytest
from server import redis_client

auth_credentials = {
    "username":"azr1",
    "password":"20S0KPNOIM"
}
req = [
    {
    "inbound_data":{
        "to":"4924195509198",
        "from":"123126",
        "text":"STOP"
    },
    "outbound_data":{
        "to":"123126",
        "from":"4924195509198",
        "text":"HI"
    }
    },
    {
    "inbound_data":{
        "to":"4924195509196",
        "from":"123126",
        "text":"STORE"
    },
    "outbound_data":{
        "to":"123126",
        "from":"4924195509196",
        "text":"HI"
    }
    }  
]
@pytest.mark.parametrize('req',req)
def test_1_integration(flask_app, req):
    url_inbound = '/inbound/sms'
    headers = {'Content-type': 'application/json'}
    response_inbound = flask_app.post(url_inbound,auth=(auth_credentials["username"],auth_credentials["password"]),json=req["inbound_data"],headers = headers)
    url_outbound = '/outbound/sms'
    hash_outbound_stop= f"STOP_{req['outbound_data']['to']}:{req['outbound_data']['from']}"
    hash_inbound_stop = f"STOP_{req['inbound_data']['from']}:{req['inbound_data']['to']}"
    response_outbound = flask_app.post(url_outbound,auth=(auth_credentials["username"],auth_credentials["password"]),json=req["outbound_data"],headers = headers)  
    if(redis_client.hget(hash_outbound_stop,req["outbound_data"]["to"])):
        assert response_inbound.status_code == 200 and response_outbound.get_json()["error"]
        # redis_client.delete(hash_outbound_stop)
    else:
        # redis_client.delete(hash_inbound_stop)
        assert response_inbound.status_code == 200 and not response_outbound.get_json()["error"] 

