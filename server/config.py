from dotenv import load_dotenv
load_dotenv()
import os 
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

class Config(object):
    DEBUG=False
    TESTING=False
    SECRET_KEY = ";a;d2123-a2032-123"
    DB_HOST = os.environ["DB_HOST"]
    DB_USER = os.environ["DB_USER"]
    DB_PASS = os.environ["DB_PASS"]
    REDIS_HOST="0.0.0.0"
    REDIS_PORT= "6379"
    DB_NAME = "production-db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DB_NAME = Config.DB_NAME
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=Config.DB_USER,pw=Config.DB_PASS,url=Config.DB_HOST,db=DB_NAME)
    REDIS_DB = "0"

class DevelopmentConfig(Config):
    DEBUG=True
    DB_NAME = "development-db"
    REDIS_DB = "1"
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=Config.DB_USER,pw=Config.DB_PASS,url=Config.DB_HOST,db=DB_NAME)

class TestingConfig(Config):
    TESTING=True
    DB_NAME="testing-db"
    REDIS_DB = "2"
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=Config.DB_USER,pw=Config.DB_PASS,url=Config.DB_HOST,db=DB_NAME)
    