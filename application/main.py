import re
from flask import Blueprint, render_template,request,redirect,url_for,jsonify,make_response,flash
from application import db,app,mysql
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, current_user
from application.models import User
import datetime
from application import models
#chatbot
import nltk,pickle,json,random;nltk.download('popular')
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import numpy as np 
intents = json.loads(open('application/content.json').read())
words = pickle.  load(open('texts.pkl','rb'))
classes = pickle.load(open('labels.pkl','rb'))
#upload gambar
from werkzeug.utils import secure_filename
import os,glob,urllib.request

main = Blueprint('main', __name__)
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
img_list=glob.glob("/content/drive/MyDrive/dataset/anorganik/*.jpg")
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@main.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    else:
        return render_template('index.html')
@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('admin/index.html', name=current_user.name)


@main.route("/admin/<id>/edit", methods=["GET"])
@login_required
def edit(tid):
    admin = models.query.filter_by(id=id).first()
    data_admin = models.query.all()
    return render_template("admin/edit.html", admin=admin, data_admin=data_admin)

@main.route("/admin/update", methods=["POST"])
@login_required
def update():
    newname = request.form.get("newname")
    oldname = request.form.get("oldname")
    admin = models.query.filter_by(name=oldname).first()
    admin.name = newname
    newemail = request.form.get("newemail")
    oldemail = request.form.get("oldemail")
    admin = models.query.filter_by(email=oldemail).first()
    admin.email = newemail
    newpassword = request.form.get("newpassword")
    oldpassword = request.form.get("oldpassword")
    newpassword = generate_password_hash(newpassword, method='sha256')
    admin = models.query.filter_by(password=oldpassword).first()
    admin.password = newpassword
    db.session.commit()
    return redirect("/admin/admin")
@main.route("/admin/delete", methods=["POST"])
@login_required
def delete():
    id = request.form.get("id")
    admin = models.query.filter_by(title=title).first()
    db.session.delete(admin)
    db.session.commit()
    return redirect("/dashboard")
@main.route('/admin/warga',methods=['GET'])
@login_required
def warga():
    warga = mysql.connection.cursor()
    warga.execute("SELECT * FROM data_warga")
    data_warga = warga.fetchall()
    warga.close()
    return render_template('admin/data_warga.html',data_warga=data_warga)
@main.route('/deleteuser/<id>')
@login_required
def deleteuser(id):
    try:
        if request.method == 'GET':
            warga = mysql.connection.cursor()
            warga.execute("DELETE FROM data_warga where id = "+id)
            mysql.connection.commit()
    except Exception as e:
        return make_response(e)
    return redirect(url_for('main.warga'))
@main.route('/formupdate/<id>', methods=['GET'])
@login_required
def formupdate(id):
    warga = mysql.connection.cursor()
    warga.execute("SELECT * FROM data_warga where id ="+id)
    data_warga = warga.fetchall()
    warga.close()
    print(data_warga)
    return render_template('admin/edit_warga.html',data_warga=data_warga)
@main.route('/updateuser/<id>',methods=['POST'])
@login_required
def updateuser(id):
    warga = mysql.connection.cursor()
    nama = request.form['nama']
    alamat = request.form['alamat']
    kontak = request.form['kontak']
    password = request.form['password']
    email = request.form['email']
    warga.execute("UPDATE data_warga SET id = "+id+",nama ='"+ nama+"',no_rumah = '" +alamat+"',kontak='"+ kontak+"',password = '"+password+"',email = '"+email+"' WHERE  id ="+id)
    mysql.connection.commit()
    data_warga = warga.fetchall()
    return redirect(url_for('main.warga',data_warga=data_warga))
@main.route('/admin/admin')
@login_required
def admin():
    users = User.query.all()
    return render_template('admin/listadmin.html',data_admin=users)
@main.route('/deleteadmin/<id>')
@login_required
def deleteadmin(id):
    try:
        if request.method == 'GET':
            warga = mysql.connection.cursor()
            warga.execute("DELETE FROM data_warga where id = "+id)
            mysql.connection.commit()
    except Exception as e:
        return make_response(e)
    return redirect(url_for('main.warga'))
@main.route('/formupdateadmin/<id>', methods=['GET'])
@login_required
def formupdateadmin(id):
    warga = mysql.connection.cursor()
    warga.execute("SELECT * FROM data_warga where id ="+id)
    data_warga = warga.fetchall()
    warga.close()
    print(data_warga)
    return render_template('admin/edit_warga.html',data_warga=data_warga)
@main.route('/updateadmin/<id>',methods=['POST'])
@login_required
def updateadmin(id):
    warga = mysql.connection.cursor()
    nama = request.form['nama']
    alamat = request.form['alamat']
    kontak = request.form['kontak']
    password = request.form['password']
    email = request.form['email']
    warga.execute("UPDATE data_warga SET id = "+id+",nama ='"+ nama+"',no_rumah = '" +alamat+"',kontak='"+ kontak+"',password = '"+password+"',email = '"+email+"' WHERE  id ="+id)
    mysql.connection.commit()
    data_warga = warga.fetchall()
    return redirect(url_for('main.warga',data_warga=data_warga))
@main.route('/atributuser/<jenis>',methods=['POST'])
def atributuser(jenis):
    warga = mysql.connection.cursor()
    user = request.form['user']
    berat = request.form['berat(KG)']
    gram = "gram"
    warga.execute("INSERT INTO akumulasi (jenis,user,berat,satuan) values (%s,%s,%s,%s)",(jenis,user,berat,gram,))
    mysql.connection.commit()
    return "Hasil Scan Telah Disimpan"
@main.route('/admin/anorganik')
@login_required
def anorganik():
    warga = mysql.connection.cursor()
    warga.execute("SELECT * FROM akumulasi WHERE jenis = 'anorganik'")
    data_warga = warga.fetchall()
    warga.close()
    return render_template('admin/anorganik.html', akumulasi=data_warga,anorganik=True)
@main.route('/deletesampah/<id>', methods=['GET'])
@login_required
def deletesampah(id):
    warga = mysql.connection.cursor()
    warga.execute("SELECT jenis FROM akumulasi WHERE id = "+id)
    jenis= warga.fetchone()
    if str(jenis)=="('anorganik',)":
        warga.execute("DELETE FROM akumulasi WHERE id = "+id)
        mysql.connection.commit()
        return redirect(url_for('main.anorganik'))
    elif str(jenis)=="('organik',)":
        warga.execute("DELETE FROM akumulasi WHERE id = "+id)
        mysql.connection.commit()
        return redirect(url_for('main.organik'))
    elif str(jenis)=="('b3',)":
        warga.execute("DELETE FROM akumulasi WHERE id = "+id)
        mysql.connection.commit()
        return redirect(url_for('main.b3'))
    else :
        return 'id tidak ada'
@main.route('/formupdatesampah/<id>', methods=['GET'])
@login_required
def formupdatesampah(id):
    akumulasi = mysql.connection.cursor()
    akumulasi.execute("SELECT * FROM akumulasi where id ="+id)
    data_akumulasi = akumulasi.fetchall()
    akumulasi.close()
    return render_template('admin/edit_akumulasi.html',data_warga=data_akumulasi)
@main.route('/updatesampah/<id>',methods=['POST'])
@login_required
def updatesampah(id):
    akumulasi = mysql.connection.cursor()
    jenis = request.form['jenis']
    tanggal = request.form['tanggal']
    user = request.form['user']
    berat = request.form['berat']
    satuan = request.form['satuan']
    akumulasi.execute("UPDATE akumulasi SET jenis ='"+ jenis+"',timestap= '" +tanggal+"',user='"+ user+"',berat = '"+berat+"',satuan = '"+satuan+"' WHERE  id ="+id)
    mysql.connection.commit()
    akumulasi = akumulasi.fetchall()
    return redirect(url_for('main.anorganik',akumulasi=akumulasi))
@main.route('/admin/organik')
@login_required
def organik():
    warga = mysql.connection.cursor()
    warga.execute("SELECT * FROM akumulasi WHERE jenis = 'organik'")
    data_warga = warga.fetchall()
    warga.close()
    return render_template('admin/organik.html', akumulasi=data_warga,organik=True)
@main.route('/deleteorganik/<id>')
@login_required
def deleteorganik(id):
    try:
        if request.method == 'GET':
            warga = mysql.connection.cursor()
            warga.execute("DELETE FROM akumulasi where id = "+id)
            mysql.connection.commit()
    except Exception as e:
        return make_response(e)
    return redirect(url_for('main.organik'))
@main.route('/admin/b3')
@login_required
def b3():
    warga = mysql.connection.cursor()
    warga.execute("SELECT * FROM akumulasi WHERE jenis = 'b3'")
    data_warga = warga.fetchall()
    warga.close()
    return render_template('admin/b3.html', akumulasi=data_warga,b3=True)
@main.route('/deleteb3/<id>')
@login_required
def deleteb3(id):
    try:
        if request.method == 'GET':
            warga = mysql.connection.cursor()
            warga.execute("DELETE FROM akumulasi where id = "+id)
            mysql.connection.commit()
    except Exception as e:
        return make_response(e)
    return redirect(url_for('main.b3'))
@main.route('/history/<username>', methods=['GET'])
def historyuser_post(username):
    warga = mysql.connection.cursor()
    warga.execute("SELECT timestap,jenis,count(berat) as jumlah,user FROM akumulasi WHERE user = %s GROUP BY jenis" , (username,))
    history = warga.fetchall()
    warga.execute("SELECT timestap, jenis,SUM(berat)/1000 as akumulasi,user FROM akumulasi WHERE user = %s GROUP BY jenis" , (username,))
    berat = warga.fetchall()
    return render_template('history.html',history=history,berat=berat)
