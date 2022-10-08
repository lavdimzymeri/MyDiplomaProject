import os
from flask.templating import render_template
from flask import Flask
from flask_mail import Mail
from flask_session import Session
from flask_admin.base import AdminIndexView
from flask_bootstrap import Bootstrap
from flask_oauthlib.client import OAuth
from flask_login import LoginManager, current_user
from flask_admin import Admin, expose, BaseView
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy.model import Model
from werkzeug.utils import redirect
from hms.config import Config
from hms import main
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)

login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.session_protection = "strong"

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.username=='Adminpersonnel' 

admin = Admin(app, index_view=MyAdminIndexView(),template_mode='bootstrap3')
oauth = OAuth()
mail = Mail(app)
sess = Session(app)


def create_app():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://hmsadmin:hmsadmin@localhost/hmsdb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SESSION_TYPE'] = 'sqlalchemy'
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    app.config['MAIL_SERVER'] = "smtp.gmail.com"
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = 'hospitalmanagersystem@gmail.com'
    app.config['MAIL_PASSWORD'] = 'oxxqbowmpudyzvcn'
    db.init_app(app)
    app.config['SESSION_SQLALCHEMY'] = db
    sess.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    oauth.init_app(app)
    bootstrap = Bootstrap(app)
    
    
    app.secret_key = Config.SECRET_KEY
    
    from hms.main.routes import main
    from hms.users.routes import users

    app.register_blueprint(main)
    app.register_blueprint(users)

    return app