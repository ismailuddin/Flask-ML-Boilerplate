from enum import Enum
from datetime import datetime
from typing import List
from sqlalchemy import exc
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login_manager

class UserRoles(Enum):
    VIEWER = 100
    USER = 200
    MANAGER = 300
    ADMIN = 900

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.Enum(UserRoles), default=UserRoles.USER)
    jobs = db.relationship('Job', backref="user", lazy="dynamic")
    date_created = db.Column(
        db.DateTime, index=True, default=datetime.utcnow
    )
    date_modified = db.Column(
        db.DateTime, index=True, default=datetime.utcnow
    )

    def __repr__(self) -> str:
        return "<User {}>".format(self.email)

    def is_admin(self) -> bool:
        return True if self.role == UserRoles.ADMIN else False

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)
        return

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def get_jobs(self) -> List['Job']:
        return self.jobs

    @classmethod
    def create_user(cls, **kwargs) -> 'User':
        user = cls(
            first_name=kwargs["first_name"],
            last_name=kwargs["last_name"],
            email=kwargs["email"]
        )
        user.set_password(kwargs["password"])
        try:
            db.session.add(user)
            db.session.commit()
        except exc.SQLAlchemyError:
            db.session.rollback()
            return None
        return user


@login_manager.user_loader
def load_user(id: str) -> User:
    return User.query.get(int(id))
