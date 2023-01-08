from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL 
from . import settings
from flask_cors import CORS

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()
mysql = MySQL()
UPLOAD_FOLDER = 'application/static/upload/'
app = Flask(__name__)
# app.config['SECRET_KEY'] = 'secret-key-goes-here'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= True
# app.config['MYSQL_DATABASE_HOST']= 'us-mm-auto-dca-05-a.cleardb.net'
# app.config['MYSQL_DATABASE_USER'] = 'bccc1e5d68a972'
# app.config['MYSQL_DATABASE_PASSWORD']  = '29f342a476deb48'
# app.config['MYSQL_DATABASE_DB'] = 'heroku_068afdbbc88db22'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config.update(dict(
SECRET_KEY="powerful secretkey",
WTF_CSRF_SECRET_KEY="dudu rohosio"
    ))
login_manager = LoginManager()
# login_manager.login_view = 'auth.login'
login_manager.init_app(app)
login_manager.login_message = u"selamat datang"
login_manager.login_message_category = "info"
from application.models import User

@login_manager.user_loader
def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))
    # blueprint for auth routes in our app
from application.auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

# blueprint for non-auth parts of app
from application.main import main as main_blueprint
app.register_blueprint(main_blueprint)
CORS(app)
# import os
# import sys
# import urllib.parse 

# # Register database schemes in URLs.
# urllib.parse.uses_netloc.append('mysql')

# try:

#     # Check to make sure DATABASES is set in settings.py file.
#     # If not default to {}

#     if 'DATABASES' not in locals():
#         DATABASES = {}

#     if 'DATABASE_URL' in os.environ:
#         url = urllib.parse.urlparse(os.environ['DATABASE_URL'])

#         # Ensure default database exists.
#         DATABASES['default'] = DATABASES.get('default', {})

#         # Update with environment configuration.
#         DATABASES['default'].update({
#             'NAME': url.path[1:],
#             'USER': url.username,
#             'PASSWORD': url.password,
#             'HOST': url.hostname,
#             'PORT': url.port,
#         })

#         if url.scheme == 'mysql':
#             DATABASES['default']['ENGINE'] = 'django.db.backends.mysql'
# except Exception:
#     print ("Unexpected error:", sys.exc_info())

