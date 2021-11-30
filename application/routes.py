from enum import unique
from flask.wrappers import Response
from flask import json, render_template, request,Response, url_for, redirect
from application import app , mysql
from application.forms import LoginForm
from application.forms import LoginForm, RegisterForm

@app.route('/')
@app.route('/home')
@app.route('/index')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM mobil")
    rv = cur.fetchall()
    cur.close() 
    return render_template('index.html', mobil=rv)
@app.route('/login',methods=['GET','POST'])
def login():
    form =LoginForm()
    if request.method == "POST":
        details = request.form
        cur = mysql.connection.cursor()
        cur.execute("SELECT username FROM admin")
        nama = cur.fetchall() 
        cur.execute("SELECT password FROM admin")
        pswd = cur.fetchall()
        cur.close()
        return 
    return render_template("login.html", title="Login",form =form, login=True)
@app.route('/warga')
def warga():
    warga = mysql.connection.cursor()
    warga.execute("SELECT * FROM data_warga")
    data_warga = warga.fetchall()
    warga.close()
    return render_template('warga.html', data_warga=data_warga)
@app.route('/login/admin')
def admin():
    kabel = mysql.connection.cursor()
    kabel.execute("SELECT * FROM qna")
    tabel = kabel.fetchall()
    kabel.close()
    return render_template('/admin/index.html', admin=tabel)