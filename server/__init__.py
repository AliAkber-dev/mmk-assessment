from flask_redis import Redis
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from server import config
conf_dict = {
    "development":config.DevelopmentConfig,
    "testing":config.TestingConfig,
    "production":config.ProductionConfig
}

redis_client = Redis()
db = SQLAlchemy()

def create_app(config_name="development"):
    app = Flask(__name__)
    env = config_name
    if(app.config["ENV"] in list(conf_dict.keys())):
        env = app.config["ENV"]
    elif(config_name in list(conf_dict.keys())):
        env = config_name
    
    app.config.from_object(conf_dict[env])
    print(f"FLASK_ENV set to {env}")
    redis_client.init_app(app)
    db.init_app(app)
    return app
