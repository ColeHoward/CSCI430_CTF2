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
    # app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
    # app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
    app.config['MAIL_USERNAME'] = 'csci430team@gmail.com'
    app.config['MAIL_PASSWORD'] = 'F]Yk]f~BYv(Gx4qM'
    app.config.update(
        # SESSION_COOKIE_SECURE=True,
        # SESSION_COOKIE_HTTPONLY=True,
        # REMEMBER_COOKIE_DURATION=timedelta(minutes=25),
        # PERMANENT_SESSION_LIFETIME=timedelta(days=7),
    )

    db.init_app(app)
    print('here')
    create_database(app)

    # ensure user not logged in is directed to login page onload
    # login_manager = LoginManager()
    # login_manager.login_view = 'login'
    # login_manager.session_protection = "strong"
    # login_manager.init_app(app)

    # @login_manager.user_loader
    # def load_user(id):
    #     return User.query.get(id)
    #     # return User.query.filter_by(alternative_id=id).first()
    return app


def create_database(app):
    print('here2')
    # if not path.exists('website/' + DB_NAME):
    db.create_all(app=app)
    print('database created!')
