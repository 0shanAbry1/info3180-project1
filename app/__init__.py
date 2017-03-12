from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = "$PrOj3cT1:)"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://admin:test01@localhost/proj1"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True # added just to suppress a warning

# Storage folder - Images uploaded
UPLOAD_FOLDER = '.app/static/uploads'

db = SQLAlchemy(app)

app.config.from_object(__name__)
from app import views, models
