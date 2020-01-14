import os
from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
MIGRATIONS_DIR = os.path.join(BASE_DIR, '../migrations')

# APP CONFIG
app = Flask(__name__)
app.config['SECRET_KEY'] = "devkey"

# DATABASE CONFIG
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)
Migrate(app, db, directory=MIGRATIONS_DIR)

# EMAIL CONFIG

# API ROUTES
