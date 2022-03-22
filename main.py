from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL 
# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()
mysql = MySQL()
UPLOAD_FOLDER = 'application/static/upload/'
main = Flask(__name__)
@main.route('/')
def index():
    return "halloworld"

if __name__ == '__main__':
    main.run(host="0.0.0.0", port=5000, debug=True)