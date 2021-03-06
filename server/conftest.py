import pytest
from server import create_app
from flask_restful import Api
from server.routes.inbound import InboundAPI
from server.routes.outbound import OutboundAPI
from flask_sqlalchemy import SQLAlchemy
@pytest.fixture(scope="session")
def flask_app():
    app = create_app("testing")
    api = Api(app)
    api.add_resource(InboundAPI, '/inbound/sms')
    api.add_resource(OutboundAPI,'/outbound/sms')
    client = app.test_client()
    ctx = app.test_request_context()
    ctx.push()
    yield client
    ctx.pop()