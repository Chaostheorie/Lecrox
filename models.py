# db_creator.py
from app import db, app
from flask_user import *

# Content tables
class snippets(db.Model):
    __tablename__ = "snippets"
    __searchable__ = ["name", "type", "content", "description"]
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    type = db.Column(db.String)
    content = db.Column(db.String)
    description = db.Column(db.String)

class plans(db.Model):
# here will plans go
    __tablename__ = "plans"
    __searchable__ = ["name"]
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

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

# Auth is made in
# Init Static Users, if there are not created before
if not User.query.filter(User.username == 'admin').first():
	user = User(
		username = 'admin',
		password = user_manager.hash_password('Password1'),
    )
	user.roles.append(Role(name='Admin'))
	db.session.add(user)
	db.session.commit()
