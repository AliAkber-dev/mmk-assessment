#from server import create_app
def test_inbound_api(flask_app):
    #check for method not allowed request (405)
    url = '/inbound/sms'
    response = flask_app.get(url)
    print(response)
    assert response.status_code == 405
    #check for unauthorized access request (403)
    
    response = flask_app.post(url)
    print(response)
    #assert response.get_json() == {"msg":'HelloWorld'}
    assert response.status_code == 401