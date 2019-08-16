import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://sanii:2125@localhost/job'
    UPLOADED_PHOTOS_DEST ='app/static/photos'

    
    SIMPLEMDE_JS_IIFE = True
    SIMPLEMDE_USE_CDN = True
class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://sanii:2125@localhost/job'
    DEBUG = True

class ProdConfig(Config):
    pass
   ##SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")

class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://sanii:2125@localhost/job'

config_options = {
'development':DevConfig,
'production':ProdConfig,
'test':TestConfig
}