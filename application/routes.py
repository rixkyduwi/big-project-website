from flask import render_template, request, url_for, redirect
from application import app
from flask_mysqldb import MySQL
mysql = MySQL(app)

@app.route('/')
@app.route('/home')
@app.route('/index')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM mobil")
    rv = cur.fetchall()
    cur.close() 
    render_template('index.html', mobil=rv)
    
@app.route('/admin')
def admin():
    kabel = mysql.connection.cursor()
    kabel.execute("SELECT * FROM admin")
    tabel = kabel.fetchall()
    kabel.close()
    return render_template('login.html', admin=tabel)
@app.route('/warga')
def admin():
    warga = mysql.connection.cursor()
    warga.execute("SELECT * FROM warga")
    data_warga = warga.fetchall()
    data_warga.close()
    return render_template('warga.html', data_warga=data_warga)
