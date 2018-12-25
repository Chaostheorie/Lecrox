from flask import *
from flask_sqlalchemy import SQLAlchemy
from flask_user import *
from elasticsearch import Elasticsearch

# Config class for Apps (flask_sqlalchemy, flask_user)
class ConfigClass(object):
	# File-based SQL database
	SQLALCHEMY_DATABASE_URI = 'sqlite:///static/database/lecrox_db.sqlite'
	# Avoids SQLAlchemy warning (Can Help by Database Processing Debugging)
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	# *Not Secret* Secret Key
	SECRET_KEY = 'London Bridge is falling, my fair lady.'
	# Flask-User settings
	USER_APP_NAME = "Lecrox 0.1"
	USER_ENABLE_EMAIL = False
	USER_ENABLE_USERNAME = True
	USER_ENABLE_CHANGE_USERNAME = True
	USER_ENABLE_CHANGE_PASSWORD = True
	USER_ENABLE_REGISTER = False
	# Elasticsearch Url for Full text search
	ELASTICSEARCH_URL = "http://localhost:9200"

# init of flask
app = Flask(__name__)

# init of config class for apps
app.config.from_object(__name__+'.ConfigClass')

# init of apps
db = SQLAlchemy(app)
app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
	if app.config['ELASTICSEARCH_URL'] else None
