# db_creator.py
from app import db, app
from flask_user import *
from search import *

class SearchableMixin(object):
    @classmethod
    def search(cls, expression, page, per_page):
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)), total

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)

db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)

# Content tables
class snippets(SearchableMixin, db.Model):
    __tablename__ = "snippets"
    __searchable__ = ["name", "type", "content", "description"]
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    type = db.Column(db.String)
    content = db.Column(db.String)
    description = db.Column(db.String)

class plans(SearchableMixin,db.Model):
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
