from flask import Flask
from config import config_options,Config
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_uploads import UploadSet,configure_uploads,IMAGES


db = SQLAlchemy()
bootstrap = Bootstrap()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
photos = UploadSet('photos',IMAGES)

'''
The auth.login is the function(or endpoint) name for the login views
'''
mail = Mail()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_options[config_name])
    app.config.from_object(Config)

    bootstrap.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    # initializing flask login extension
    login_manager.init_app(app)

    #registering main blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint,url_prefix = '/authenticate')
    configure_uploads(app,photos)

    #initializing the app with the flask extensions
    return app
