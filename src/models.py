from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Users(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String, nullable=True)
    password = db.Column(db.String, nullable=False)
    files = db.relationship('File', backref='users')

    def __init__(self, login, password):
        self.login = login
        self.password = password


class File(db.Model):
    __tablename__ = 'file'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String, nullable=False)
    content = db.Column(db.LargeBinary, nullable=True)
    expire_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        server_default=db.func.current_timestamp()
    )
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    def __init__(self, filename, content, expire_at, owner_id=None):
        self.filename = filename
        self.content = content
        self.expire_at = expire_at
        self.owner_id = owner_id
