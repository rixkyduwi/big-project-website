from flask import Blueprint, render_template
from . import db
from flask_login import login_required, current_user
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

main = Blueprint('main', __name__)
@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('admin/index.html', name=current_user.name)
@main.route('/admin/warga')
@login_required
def warga():
    warga = mysql.connection.cursor()
    warga.execute("SELECT * FROM data_warga")
    data_warga = warga.fetchall()
    warga.close()
    return render_template('admin/data_warga.html', data_warga=data_warga,warga=True)
@main.route('/admin/anorganik')
@login_required
def anorganik():
    warga = mysql.connection.cursor()
    warga.execute("SELECT * FROM data_warga")
    data_warga = warga.fetchall()
    warga.close()
    return render_template('admin/anorganik.html', data_warga=data_warga,anorganik=True)
@main.route('/admin/organik')
@login_required
def organik():
    warga = mysql.connection.cursor()
    warga.execute("SELECT * FROM data_warga")
    data_warga = warga.fetchall()
    warga.close()
    return render_template('admin/organik.html', data_warga=data_warga,organik=True)
@main.route('/admin/b3')
@login_required
def b3():
    warga = mysql.connection.cursor()
    warga.execute("SELECT * FROM data_warga")
    data_warga = warga.fetchall()
    warga.close()
    return render_template('admin/b3.html', data_warga=data_warga,b3=True)
@main.route('/admin/latih_mesin')
@login_required
def latih_mesin():
    warga = mysql.connection.cursor()
    warga.execute("SELECT * FROM data_warga")
    data_warga = warga.fetchall()
    warga.close()
    return render_template('admin/latih_mesin.html', data_warga=data_warga,latih_mesin=True)
@main.route('/admin/listadmin')
@login_required
def listadmin():
    warga = mysql.connection.cursor()
    warga.execute("SELECT * FROM data_warga")
    data_warga = warga.fetchall()
    warga.close()
    return render_template('admin/listadmin.html', data_warga=data_warga,listadmin=True)