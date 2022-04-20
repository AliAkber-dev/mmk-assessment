from dotenv import load_dotenv
load_dotenv()
import os 
class Config(object):
    DEBUG=False
    TESTING=False
    SECRET_KEY = ";a;d2123-a2032-123"
    DB_NAME = "production-db"
    DB_HOST = os.environ["DB_HOST"]
    REDIS_URL = os.environ['REDIS_URL']
    DB_USER = os.environ["DB_USER"]
    DB_PASSWORD = os.environ["DB_PASS"]

class ProductionConfig(Config):
    pass 

class DevelopmentConfig(Config):
    DEBUG=True
    DB_NAME = "db_mmk"

class TestingConfig(Config):
    TESTING=True
    DB_NAME="testing-db"

