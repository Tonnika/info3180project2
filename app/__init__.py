from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = "this is a random key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://project2:project2@localhost/project2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


UPLOAD_FOLDER = "./app/static/uploads"

db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.config.from_object(__name__)

from app import model,views
