from flask import Blueprint, render_template, redirect, url_for,request,flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required,current_user
from application.models import User
from application import db,mysql
auth = Blueprint('auth', __name__)
# @auth.route('/login')
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('main.dashboard'))
#     else:
#         return render_template('login.html')
# @auth.route('/login', methods=['PUT','POST'])
# def login_post():
#         #digunakan untuk login user db mysql
#         if request.method == 'PUT':
#             warga = mysql.caonnection.cursor()
#             username = request.form['username']
#             password = request.form['password']
#             warga.execute("SELECT email FROM data_warga WHERE email= %s AND password = %s" , (username, password,))
#             user = warga.fetchall()
#             return "halo"+str(user)
#         #login untuk admin db sqlite
#         elif request.method == 'POST':
#             if form.validate_on_submit():
#                 email = request.form.get('email')
#                 password = request.form.get('password')
#                 remember = True if request.form.get('remember') else False
#                 #validasi login
#                 user = User.query.filter_by(email=email).first()

#                 # check if the user actually exists
#                 # take the user-supplied password, hash it, and compare it to the hashed password in the database
#                 if not user or not check_password_hash(user.password, password):
#                     flash('Please check your login details and try again.')#berbeda
#                     return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

#                 # if the above check passes, then we know the user has the right credentials
#                 login_user(user, remember=remember)
#                 return redirect(url_for('main.dashboard'))#sama
    
# @auth.route('/signup')
# def signup():
#     if current_user.is_authenticated:
#         return redirect(url_for('main.dashboard'))
#     else:    
#         return render_template('signup.html')
# @auth.route('/signup_post', methods=['POST'])
# def signup_post():
#         email = request.form.get('email')
#         name = request.form.get('name')
#         password = request.form.get('password')

#         user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

#         if user: # if a user is found, we want to redirect back to signup page so user can try again
#             flash('Email address already exists. go back to login')
#             return redirect(url_for('auth.signup'))
#             # create a new user with the form data. Hash the password so the plaintext version isn't saved.
#         new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))
#             # add the new user to the database
#         db.session.add(new_user)
#         db.session.commit()
#         return redirect(url_for('auth.login'))
    
# @auth.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('main.index'))
# @auth.route('/reguser/<username>', methods=['POST'])
# def reguser(username):
#     warga = mysql.connection.cursor()
#     nama = request.form['nama']
#     email = request.form['email']
#     password = request.form['password']
#     no_rumah = request.form['no_rumah']
#     kontak = request.form['kontak']
#     warga.execute("INSERT INTO data_warga (nama,email,password,no_rumah,kontak) values (%s,%s,%s,%s,%s)",(nama,email,password,no_rumah,kontak,))
#     mysql.connection.commit()
#     return "halo"+str(nama)
