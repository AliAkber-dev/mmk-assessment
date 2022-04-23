from server import create_app
from flask_restful import Api
from server.routes.inbound import InboundAPI
from server.routes.outbound import OutboundAPI
#from waitress import serve
app = create_app()
api = Api(app)
api.add_resource(InboundAPI, '/inbound/sms')
api.add_resource(OutboundAPI,'/outbound/sms')
if __name__ == "__main__":
    app.run(host="127.0.0.1",port=5000)