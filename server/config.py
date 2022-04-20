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
    DB_PASS = os.environ["DB_PASS"]
    SQLALCHEMY_TRACK_MODIFICATIONS = False
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=Config.DB_USER,pw=Config.DB_PASS,url=Config.DB_HOST,db=Config.DB_NAME)
    pass 

class DevelopmentConfig(Config):
    DEBUG=True
    DB_NAME = "db_mmk"
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=Config.DB_USER,pw=Config.DB_PASS,url=Config.DB_HOST,db=Config.DB_NAME)
    
class TestingConfig(Config):
    TESTING=True
    DB_NAME="testing-db"
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=Config.DB_USER,pw=Config.DB_PASS,url=Config.DB_HOST,db=Config.DB_NAME)
    

