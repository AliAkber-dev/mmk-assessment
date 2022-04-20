from server import app
test_client = app.test_client()

def test_inbound_api():
    url = '/'
    response = test_client.get(url)
    assert response.get_data() == b'Hello World'
    assert response.status_code == 200