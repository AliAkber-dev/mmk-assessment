from flask_redis import FlaskRedis
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from server import config
from flask_restful import Api
app = Flask(__name__)
redis_client = FlaskRedis(app)
if(app.config["ENV"]=="development"):
    print("FLASK_ENV set to ",app.config["ENV"])
    app.config.from_object(config.DevelopmentConfig)

db = SQLAlchemy(app)
api = Api(app)