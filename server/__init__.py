from flask_redis import FlaskRedis
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from server import config

conf_dict = {
    "development":config.DevelopmentConfig,
    "testing":config.TestingConfig,
    "production":config.ProductionConfig
}

redis_client = FlaskRedis()
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    if(app.config["ENV"] in list(conf_dict.keys())):
        app.config.from_object(conf_dict[app.config["ENV"]])
        print(f"FLASK_ENV set to {app.config['ENV']}")
        redis_client.init_app(app)
        db.init_app(app)
    return app
