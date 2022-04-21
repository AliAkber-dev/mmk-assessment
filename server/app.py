from server import create_app
from flask_restful import Api
from server.routes.inbound import InboundAPI
from server.routes.outbound import OutboundAPI
app = create_app()
api = Api(app)
api.add_resource(InboundAPI, '/inbound/sms')
api.add_resource(OutboundAPI,'/outbound/sms')
api.add_resource(Hello,'/')
if __name__ == "__main__":
    app.run(host="127.0.0.1",port=8080, debug=True)