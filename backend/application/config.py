from datetime import timedelta
import os

class Config(object):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'
    SECRET_KEY = os.getenv('SECRET_KEY')
    
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_COOKIE_SECURE = False
    JWT_TOKEN_LOCATION = ['headers','cookies']
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=2)
    JWT_SESSION_COOKIE = False  
    JWT_ACCESS_COOKIE_EXPIRES = timedelta(hours=2)
    BUNDLE_ERRORS = True
    PROPAGATE_EXCEPTIONS = True
    JWT_ACCESS_COOKIE_PATH = '/'
    JWT_COOKIE_CSRF_PROTECT = True
    JWT_COOKIE_SAMESITE = None 
    JWT_CSRF_IN_COOKIES = True  
    JWT_CSRF_COOKIE_HTTPONLY = False  
    JWT_CSRF_CHECK_FORM = True
    JWT_COOKIE_DOMAIN = '.localhost'

    MAIL_SERVER = 'smtp.gmail.com'  
    MAIL_PORT = 587  
    MAIL_USE_TLS = True  
    MAIL_USE_SSL = False  
    MAIL_NAME="HomeGenie"
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')

    CACHE_TYPE =  "RedisCache"
    CACHE_DEFAULT_TIMEOUT = 30
    CACHE_REDIS_PORT = 6379


