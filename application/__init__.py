from flask import Flask 
from flask_mysqldb import MySQL 
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'big_project'
app.config.update(dict(
  SECRET_KEY="powerful secretkey",
  WTF_CSRF_SECRET_KEY="a csrf secret key"
))
mysql = MySQL(app)
from application import routes