from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class File(db.Model):
    __tablename__ = 'file'

    id = db.Column(db.Integer, primary_key=True)
    file = db.Column(db.LargeBinary, nullable=True)
    live_time = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        server_default=db.func.current_timestamp()
    )
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    def __init__(self, file, live_time, owner_id):
        self.file = file
        self.live_time = live_time
        self.owner_id = owner_id


class Users(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String, nullable=True)
    password = db.Column(db.String, nullable=False)
    files = db.relationship('File', backref='users')

    def __init__(self, login, password):
        self.login = login
        self.password = password
