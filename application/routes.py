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
        passs=details['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT username FROM admin") 
        if (details['username']== cur.fetchall() ):
            cur.execute("SELECT username FROM admin") 
            if (passs == cur.fetchall() ):
                cur.close()
                return redirect('/login/admin')

            else:
                cur.close()
                return render_template("login.html",a="password salah", title="Login",form =form, login=True)
        else:
            return render_template("login.html", a="user/pswd salah",title="Login",form =form, login=True)
    return render_template("login.html", title="Login",form =form, login=True)
@app.route('/login/admin')
def admin():
    kabel = mysql.connection.cursor()
    kabel.execute("SELECT * FROM qna")
    tabel = kabel.fetchall()
    kabel.close()
    return render_template('admin/index.html', admin=tabel)
@app.route('/admin/warga')
def warga():
    warga = mysql.connection.cursor()
    warga.execute("SELECT * FROM data_warga")
    data_warga = warga.fetchall()
    warga.close()
    return render_template('admin/data_warga.html', data_warga=data_warga,warga=True)
@app.route('/admin/anorganik')
def anorganik():
    warga = mysql.connection.cursor()
    warga.execute("SELECT * FROM data_warga")
    data_warga = warga.fetchall()
    warga.close()
    return render_template('admin/anorganik.html', data_warga=data_warga,anorganik=True)
@app.route('/admin/organik')
def organik():
    warga = mysql.connection.cursor()
    warga.execute("SELECT * FROM data_warga")
    data_warga = warga.fetchall()
    warga.close()
    return render_template('admin/organik.html', data_warga=data_warga,organik=True)
@app.route('/admin/b3')
def b3():
    warga = mysql.connection.cursor()
    warga.execute("SELECT * FROM data_warga")
    data_warga = warga.fetchall()
    warga.close()
    return render_template('admin/b3.html', data_warga=data_warga,b3=True)
@app.route('/admin/latih_mesin')
def latih_mesin():
    warga = mysql.connection.cursor()
    warga.execute("SELECT * FROM data_warga")
    data_warga = warga.fetchall()
    warga.close()
    return render_template('admin/latih_mesin.html', data_warga=data_warga,latih_mesin=True)
@app.route('/admin/listadmin')
def listadmin():
    warga = mysql.connection.cursor()
    warga.execute("SELECT * FROM data_warga")
    data_warga = warga.fetchall()
    warga.close()
    return render_template('admin/listadmin.html', data_warga=data_warga,listadmin=True)


