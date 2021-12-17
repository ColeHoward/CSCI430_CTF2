# this file makes 'websites' a python package... meaning we can import it
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from website.databases import db

# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

DB_NAME = "database.db"
EMAIL_USER = 'csci430team@gmail.com'
EMAIL_PASS = 'F]Yk]f~BYv(Gx4qM'


# initialize app
def create_app():
    app = Flask(__name__)
    # encrypt session data
    app.config['SECRET_KEY'] = ']TZ6kf8E9VV{~jCeTu~.]nZytGamY'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DB_NAME
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_TLS'] = True
    app.config['MAIL_DEBUG'] = True
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = 'csci430team@gmail.com'
    app.config['MAIL_PASSWORD'] = 'F]Yk]f~BYv(Gx4qM'
    app.config.update(
        # SESSION_COOKIE_SECURE=True,
        # SESSION_COOKIE_HTTPONLY=True,
        # REMEMBER_COOKIE_DURATION=timedelta(minutes=25),
        # PERMANENT_SESSION_LIFETIME=timedelta(days=7),
    )

    db.init_app(app)
    create_database(app)
    
    return app


def create_database(app):
    # if not path.exists('website/' + DB_NAME):
    db.create_all(app=app)
