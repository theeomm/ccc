import os
from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_security import Security, SQLAlchemyUserDatastore
from flask_jwt import JWT

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
MIGRATIONS_DIR = os.path.join(BASE_DIR, '../migrations')
DB_PATH = os.path.join(BASE_DIR, '../db.sqlite')

# APP CONFIG
app = Flask(__name__)
app.config['SECRET_KEY'] = "devkey"

# DATABASE CONFIG
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_PATH}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db, directory=MIGRATIONS_DIR)

# FLASK SECURITY (AUTH)
from app.auth.models import User, Role
datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, datastore)

# FLASK JWT CONFIG
from app.auth.utils import authenticate, identity
jwt = JWT(app, authenticate, identity)

# EMAIL CONFIG

# API ROUTES
from app.auth.api import UserAPI
from app.timetable.api import (
    SubjectAPI,
    SessionAPI,
    ClassAPI,
)

# Authentication Endpoints
app.add_url_rule(
    '/auth/login',
    view_func=UserAPI.as_view('login'),
    methods=['POST'],
)

# Class Endpoints
app.add_url_rule(
    '/classes',
    view_func=ClassAPI.as_view('classes')
)

app.add_url_rule(
    '/classes/<id>',
    view_func=ClassAPI.as_view('class')
)

# Subject Endpoints
app.add_url_rule(
    '/subjects',
    # defaults={'id': None},
    view_func=SubjectAPI.as_view('subjects'),
)

app.add_url_rule(
    '/subjects/<id>',
    view_func=SubjectAPI.as_view('subject'),
)

# Class Session Endpoint
app.add_url_rule(
    '/sessions',
    view_func=SessionAPI.as_view('sessions'),
)

app.add_url_rule(
    '/sessions/<id>',
    view_func=SessionAPI.as_view('session'),
)
