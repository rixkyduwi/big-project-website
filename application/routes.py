from enum import unique
from flask.wrappers import Response
from flask import json, render_template, request,Response, url_for, redirect
from application import app , mysql
from application.forms import LoginForm
from application.forms import LoginForm, RegisterForm
qna=json({"intents": [
        {"tag": "greeting",
         "patterns": ["Hi", "Is anyone there?", "Hello", "Good day"],
         "responses": ["Hello!", "Good to see you again!", "Hi there, how can I help?"],
         "context_set": ""
        },
        {"tag": "greetingMore",
         "patterns": [ "How are you", "Whats up"],
         "responses": ["I am fine!, How about you?", "I am good, you?"],
         "context_set": ""
        },
        {"tag": "goodbye",
         "patterns": ["cya", "Bye", "See you later", "Goodbye", "I am Leaving", "Have a Good day"],
         "responses": ["Sad to see you go :(", "Talk to you later", "Goodbye!"],
         "context_set": ""
        },
        {"tag": "age",
         "patterns": ["how old", "how old is John", "what is your age", "how old are you", "age?"],
         "responses": ["I am 25 years old!", "18 years young!"],
         "context_set": ""
        },
        {"tag": "name",
         "patterns": ["what is your name", "what should I call you", "whats your name?"],
         "responses": ["You can call me John.", "I'm John!", "I'm John aka John Doe."],
         "context_set": ""
        },
        {"tag": "shop",
         "patterns": ["Id like to buy something", "whats on the menu", "what do you reccommend?", "could i get something to eat"],
         "responses": ["We sell chocolate chip cookies for $2!", "Cookies are on the menu!"],
         "context_set": ""
        },
        {"tag": "hours",
         "patterns": ["when are you guys open", "what are your hours", "hours of operation"],
         "responses": ["We are open 7am-4pm Monday-Friday!"],
         "context_set": ""
        }
   ]
}) 
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


