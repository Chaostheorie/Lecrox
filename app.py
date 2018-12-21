from flask import *
from flask_sqlalchemy import SQLAlchemy
from flask_user import *

# Config class for Apps (flask_sqlalchemy, flask_user)
class ConfigClass(object):
	# File-based SQL database
	SQLALCHEMY_DATABASE_URI = 'sqlite:///static/database/lecrox_db.sqlite'
	# Avoids SQLAlchemy warning (Can Help by Database Processing Debugging)
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	# *Not Secret* Secret Key 
	SECRET_KEY = 'London Bridge is falling, my fair lady.'
	# Flask-User settings
	USER_APP_NAME = "Lecrox"
	USER_ENABLE_EMAIL = False
	USER_ENABLE_USERNAME = True
	USER_ENABLE_CHANGE_USERNAME = True
	USER_ENABLE_CHANGE_PASSWORD = True
	USER_ENABLE_REGISTER = False

# init of flask
app = Flask(__name__)

# init of config class for apps
app.config.from_object(__name__+'.ConfigClass')

# init of apps
db = SQLAlchemy(app)

# Define the User Model
class User(db.Model, UserMixin):
	# User table
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')
	username = db.Column(db.String(50, collation='NOCASE'), nullable=False, unique=True, server_default='')
	password = db.Column(db.String(255), nullable=False, server_default='')

	# Define the relationship to Role via UserRoles
	roles = db.relationship('Role', secondary='user_roles')

# Define the Role data-model
class Role(db.Model):
	__tablename__ = 'roles'
	id = db.Column(db.Integer(), primary_key=True)
	name = db.Column(db.String(50), server_default='user')

# Define the UserRoles association table
class UserRoles(db.Model):
	__tablename__ = 'user_roles'
	id = db.Column(db.Integer(), primary_key=True)
	user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
	role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))

# create tables
db.create_all()

# Setup Flask-User and specify the User data-model
user_manager = UserManager(app, db, User)

# Init Static Users, if there are not created before
if not User.query.filter(User.username == 'admin').first():
	user = User(
		username = 'admin',
		password = user_manager.hash_password('Password1'),
    )
	user.roles.append(Role(name='Admin'))
	db.session.add(user)
	db.session.commit()
