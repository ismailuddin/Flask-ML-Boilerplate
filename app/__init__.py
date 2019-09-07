from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from celery import Celery
from app.config import Config

app = Flask(__name__, static_folder="../public", static_url_path="/public")
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)

# Celery setup
celery = Celery(
    app.name,
    broker=app.config["CELERY_BROKER_URL"],
    backend=app.config["CELERY_RESULT_BACKEND"]
)

from app.routes import general
from app.routes.auth import auth
from app.models import users, jobs

app.register_blueprint(auth)