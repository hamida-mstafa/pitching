import os

class Config:
    SQLALCHEMY_DATABASE_URI ='postgresql+psycopg2://moringaschoolcom:mids@localhost/pitches'
    SECRET_KEY=os.environ.get('SECRET_KEY') or '2015'
    MAIL_SERVER ='smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    UPLOADED_PHOTOS_DEST = 'app/static/photos'

class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://moringaschoolcom:mids@localhost/pitches'

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI ='postgresql+psycopg2://moringaschoolcom:mids@localhost/pitches'
    DEBUG = True
class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI ='postgresql+psycopg2://moringaschoolcom:mids@localhost/test'
    pass


config_options = {
    'development':DevConfig,
    'production':ProdConfig,
    'test':TestConfig,

}
