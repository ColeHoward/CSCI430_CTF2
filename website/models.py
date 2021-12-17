from website.databases import db
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from .app_creation import app


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    balance = db.Column(db.Integer)
    action_type = db.Column(db.String(10))
    is_authenticated = db.Column(db.Boolean)

    def get_reset_token(self, expires_seconds=900):
        s = Serializer(app.config['SECRET_KEY'], expires_seconds)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    def __str__(self):
        return "user:" + " " + self.username + " " + self.password

    # def get_id(self):
    # return str(self.alternative_id)
