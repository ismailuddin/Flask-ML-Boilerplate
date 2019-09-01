from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    date_created = db.Column(db.DateTime, index=True,
                             default=datetime.utcnow())
    date_modified = db.Column(db.DateTime, index=True,
                              default=datetime.utcnow())

    def __repr__(self) -> str:
        return "<User {}>".format(self.email)

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)
        return

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id: str) -> User:
    return User.query.get(int(id))
