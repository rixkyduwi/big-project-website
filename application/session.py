from application import app,mail,mysql
import requests
from flask import Flask, render_template, url_for, jsonify, request, redirect, session, flash, Response, make_response
from datetime import datetime
from flask_mail import Mail, Message
from cv2 import cv2
import base64
from flask_mysqldb import MySQL
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import time
import pickle

import os

from imageio.core.functions import si
from werkzeug.utils import secure_filename

#courseid=''

import csv
from datetime import datetime
#from app import courseid
import cv2
import face_recognition
import os
import numpy as np
face_cascade=cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
ds_factor=0.6
filename=''

class VideoCamera(object):
    #courseid=''
    def _init_(self):
        self.video = cv2.VideoCapture(0)

    def _del_(self):
        self.video.release()

   

    def get_frame(self):
        ap = argparse.ArgumentParser()
        ap.add_argument("-d", "--detector", required=True,
            help="path to OpenCV's deep learning face detector")
        ap.add_argument("-m", "--embedding-model", required=True,
            help="path to OpenCV's deep learning face embedding model")
        ap.add_argument("-r", "--recognizer", required=True,
            help="path to model trained to recognize faces")
        ap.add_argument("-l", "--le", required=True,
            help="path to label encoder")
        ap.add_argument("-c", "--confidence", type=float, default=0.5,
            help="minimum probability to filter weak detections")
        args = vars(ap.parse_args())

        # muat detektor wajah bersambung kami dari disk
        print("[INFO] memuat detektor wajah...")
        protoPath = os.path.sep.join([args["detector"], "deploy.prototxt"])
        modelPath = os.path.sep.join([args["detector"],
            "res10_300x300_ssd_iter_140000.caffemodel"])
        detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)

        # memuat model penyisipan wajah berseri dari serial
        print("[INFO] memuat pengenal wajah...")
        embedder = cv2.dnn.readNetFromTorch(args["embedding_model"])

        # muat model pengenalan wajah yang sebenarnya bersama dengan label enkoder
        recognizer = pickle.loads(open(args["recognizer"], "rb").read())
        le = pickle.loads(open(args["le"], "rb").read())

        # inisialisasi aliran video, lalu biarkan sensor kamera dimulai
        print("[INFO] mulai streaming video...")
        vs = VideoStream(src=0).start()
#vs = cv2.VideoCapture(args["video"])
        time.sleep(2.0)

        # mulai penaksiran throughput FPS
        fps = FPS().start()
        frame = vs.read()
        	# ambil bingkai dari aliran video berulir
	    
	#(grabbed, frame) = vs.read()
        frame = imutils.resize(frame, width=600)
        (h, w) = frame.shape[:2]

        # membangun blob dari gambar
        imageBlob = cv2.dnn.blobFromImage(
            cv2.resize(frame, (300, 300)), 1.0, (300, 300),
            (104.0, 177.0, 123.0), swapRB=False, crop=False)

        # menerapkan pendeteksi wajah berbasis pembelajaran OpenCV yang mendalam untuk melokalisasi
        # wajah pada gambar input
        detector.setInput(imageBlob)
        detections = detector.forward()

        # loop atas deteksi
        for i in range(0, detections.shape[2]):
            # ekstrak kepercayaan (mis., probabilitas) yang terkait dengan
            # prediksi
            confidence = detections[0, 0, i, 2]

            # saring deteksi lemah
            if confidence > args["confidence"]:
                # menghitung (x, y) -koordinat dari kotak pembatas untuk
                # muka
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                # ekstrak ROI wajah
                face = frame[startY:endY, startX:endX]
                (fH, fW) = face.shape[:2]

                # Pastikan lebar dan tinggi wajah cukup besar
                if fW < 20 or fH < 20:
                    continue

                # buat gumpalan untuk ROI wajah, lalu lewati gumpalan
                # melalui model penyisipan wajah kami untuk mendapatkan 128-d
                # kuantifikasi wajah
                faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255,
                    (96, 96), (0, 0, 0), swapRB=True, crop=False)
                embedder.setInput(faceBlob)
                vec = embedder.forward()

                # melakukan klasifikasi untuk mengenali wajah
                preds = recognizer.predict_proba(vec)[0]
                j = np.argmax(preds)
                proba = preds[j]
                name = le.classes_[j]

                # menggambar kotak pembatas wajah bersama dengan
                # kemungkinan terkait
                text = "{}: {:.2f}%".format(name, proba * 100)
                y = startY - 10 if startY - 10 > 10 else startY + 10
                cv2.rectangle(frame, (startX, startY), (endX, endY),
                    (0, 255, 0), 2)
                cv2.putText(frame, text, (startX, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 255), 2)

                print("Hasil deteksi : ", name)

        # perbarui penghitung FPS
        fps.update()

        # perlihatkan frame output
        cv2.imshow("Frame", frame)
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

#obj=VideoCamera()
#courseid=fgetcourseid()
def markAttendance(name):
    #csv.DictWriter(result.csv, )
    global filename
    print(filename)
    with open('C:/xampp/htdocs/attendance/'+filename, 'r+') as f:
        dataList = f.readlines()
        nameList = []

        for line in dataList:
            entry = line.split(',')
            nameList.append(entry[0])
            print(nameList)
        if name not in nameList:
            now = datetime.now()
            dt = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dt}')







@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/login",methods=["GET","POST"])
def login():
    return render_template('login.html')

@app.route("/forgetpassword",methods=["GET","POST"])
def forgetpassword():
    if request.method == "POST":
        username = request.form['username']
        email = request.form['m_email']
        cur = mysql.connection.cursor()
        cur.execute("SELECT  password FROM logindata WHERE username=%s ",
                    (username,))
        mypassword= cur.fetchone()


        cur = mysql.connection.cursor()
        cur.execute("SELECT  emailid FROM studentdetails WHERE username=%s ",
                    (username,))
        myemail = cur.fetchone()
        m1=myemail[0]

        print(myemail[0])
        print(email)


        if email==m1:
            msg = Message('Hello', sender='chintandarji0712@gmail.com', recipients=[m1])
            msg.body = "Hello"+str(username)+"your password is"+str(mypassword[0])
            mail.send(msg)
            return redirect(url_for('login'))
        else:
            return 'please Enter Valid Email and Username'

@app.route("/user",methods=["GET","POST"])
def user():

    if request.method=="POST":
        username=request.form['username']
        password=request.form['password']
        role=request.form['role']
        cur = mysql.connection.cursor()
        cur.execute("SELECT  * FROM logindata WHERE username=%s AND password=%s AND role=%s",(username,password,role))
        data = cur.fetchone()
        cur.close()
        if data:
            session['loggedin'] = True
            session['username']=username
            session['role']=role
            session['password']=password
            return redirect(url_for('show'))

        else:
            return 'invalid username/password try again'
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username',None)
    session.pop('role',None)
    return redirect(url_for('login'))
@app.route('/show')
def show():
    if 'loggedin' in session:
        role=session.get('role')
        if role=='student':
            username = session.get('username')
            cur = mysql.connection.cursor()
            cur.execute("SELECT  * FROM studentdetails WHERE username=%s ",
                        (username,))
            data = cur.fetchone()

            cur.close()


            return render_template('student.html',username=session.get('username'),data=data)
        elif role=='faculty':
            username = session.get('username')
            cur = mysql.connection.cursor()
            cur.execute("SELECT  * FROM facultydetails WHERE username=%s ",
                        (username,))
            data = cur.fetchone()

            cur.close()
            cur = mysql.connection.cursor()
            cur.execute("SELECT courseid FROM coursedetails WHERE facultyname=%s ",
                        (username,))
            data1 = cur.fetchall()
            cur.close()

            return render_template('faculty.html', username=session.get('username'),data=data,data1=data1)
        elif role=='admin':
                cur = mysql.connection.cursor()
                cur.execute("SELECT  * FROM studentdetails")
                data = cur.fetchall()
                cur.close()
                cur = mysql.connection.cursor()
                cur.execute("SELECT  * FROM facultydetails")
                fdata = cur.fetchall()
                cur.close()
                cur = mysql.connection.cursor()
                cur.execute("SELECT  * FROM coursedetails")
                fdata1 = cur.fetchall()
                cur.close()
                cur = mysql.connection.cursor()
                cur.execute("SELECT username FROM facultydetails")
                fdata2 = cur.fetchall()
                cur.close()

                return render_template('admin.html', username=session.get('username'),students=data,facultys=fdata,coursedetail=fdata1,fdata2=fdata2)
            #return redirect(url_for('admin'))
    else:
        return redirect(url_for('login'))



@app.route('/studentupdate', methods=["GET","POST"])
def studentupdate():
    if 'loggedin' in session:
        if session.get('role')=='student':
            if request.method == 'POST':

                emailid = request.form['emailid']
                batch = request.form['batch']
                dob=request.form['dob']
                username = session.get('username')
                cur = mysql.connection.cursor()
                cur.execute("""
                       UPDATE studentdetails
                       SET emailid=%s, batch=%s, dob=%s 
                       WHERE username=%s
                    """, (emailid, batch,dob,username))
                flash("Data Updated Successfully")
                mysql.connection.commit()

                return redirect(url_for('show'))
            else:
                return 'form bhari ne aavo'
        else:
            return 'please login as student'
    else:
        return 'please first login'

@app.route('/studentchangepassword', methods=["GET","POST"])
def studentchangepassword():
    if 'loggedin' in session:
        if session.get('role')=='student':
            if request.method == 'POST':

                password=request.form['password']
                username = session.get('username')
                cur = mysql.connection.cursor()
                cur.execute("""
                       UPDATE logindata
                       SET password=%s
                       WHERE username=%s
                    """, (password,username))
                flash("Data Updated Successfully")
                mysql.connection.commit()
                return redirect(url_for('show'))
            else:
                return 'form bhari ne aavo'
        else:
            return 'please login as student'
    else:
        return 'please first login'

@app.route('/facultyupdate', methods=["GET","POST"])
def facultyupdate():
    if 'loggedin' in session:
        role=session.get('role')
        if role=='faculty':
            if request.method == 'POST':
                email = request.form['email']
                phno=request.form['phno']
                username = session.get('username')
                cur = mysql.connection.cursor()
                cur.execute("""
                       UPDATE facultydetails
                       SET email=%s, ph_no=%s
                       WHERE username=%s
                    """, (email, phno,username))
                flash("Data Updated Successfully")
                mysql.connection.commit()
                return redirect(url_for('show'))
            else:
                return 'form bhari ne aavo'
        else:
            return 'please login as faculty'
@app.route('/facultychangepassword', methods=["GET","POST"])
def facultychangepassword():
    if 'loggedin' in session:
        if session.get('role')=='faculty':
            if request.method == 'POST':

                password=request.form['password']
                username = session.get('username')
                cur = mysql.connection.cursor()
                cur.execute("""
                       UPDATE logindata
                       SET password=%s
                       WHERE username=%s
                    """, (password,username))
                flash("Data Updated Successfully")
                mysql.connection.commit()
                return redirect(url_for('show'))
            else:
                return 'form bhari ne aavo'
        else:
            return 'please login as faculty'
    else:
        return 'please first login'


@app.route('/update',methods=['POST','GET'])
def update():
    if 'loggedin' in session:
        if session.get('role')=='admin':
            if request.method == 'POST':
                username = request.form['username']
                batch = request.form['batch']
                emailid = request.form['emailid']
                dob= request.form['dob']
                cur = mysql.connection.cursor()
                cur.execute("""
                       UPDATE studentdetails
                       SET  batch=%s,
                       emailid=%s, dob=%s
                       WHERE username=%s
                    """, (batch,emailid,dob,username))
                flash("Data Updated Successfully")
                mysql.connection.commit()
                return redirect(url_for('show'))
            else:
                return 'form bhari ne aavo'
        else:
            return 'please login as a admin'




@app.route('/fupdate',methods=['POST','GET'])
def fupdate():
    if 'loggedin' in session:
        if session.get('role')=='admin':
            if request.method == 'POST':
                username = request.form['username']
                email = request.form['email']
                ph_no= request.form['ph_no']
                cur = mysql.connection.cursor()
                cur.execute("""
                       UPDATE facultydetails
                       SET  email=%s,
                         ph_no=%s
                       WHERE username=%s
                    """, (email,ph_no,username))
                flash("Data Updated Successfully")
                mysql.connection.commit()
                return redirect(url_for('show'))
            else:
                return 'form bhari ne aavo'
        else:
            return 'please login as a admin'

@app.route('/insert',methods=['POST','GET'])
def insert():
    if 'loggedin' in session:
        if session.get('role')=='admin':
            if request.method == 'POST':
                username = request.form['username']
                batch = request.form['batch']
                emailid = request.form['emailid']
                dob = request.form['dob']
                password=request.form['password']
                role='student'
                cur = mysql.connection.cursor()
                cur.execute("""
                       insert into studentdetails (username,batch, emailid, dob) VALUES (%s, %s, %s,%s)
                    """, (username,batch, emailid, dob))
                flash("Data Updated Successfully")
                mysql.connection.commit()
                cur = mysql.connection.cursor()
                cur.execute("""
                                       insert into logindata (username,password,role) VALUES (%s, %s, %s)
                                    """, (username, password,role))
                mysql.connection.commit()

                return redirect(url_for('show'))
            else:
                return 'form bhari ne aavo'
        else:
            return 'please login as admin'

@app.route('/finsert',methods=['POST','GET'])
def finsert():
    if 'loggedin' in session:
        if session.get('role')=='admin':
            if request.method == 'POST':
                username = request.form['username']
                email = request.form['email']
                phno = request.form['phno']
                password=request.form['password']
                role='faculty'
                cur = mysql.connection.cursor()
                cur.execute("""
                       insert into facultydetails (username,email,ph_no) VALUES (%s, %s, %s)
                    """, (username,email, phno))
                flash("Data Updated Successfully")
                mysql.connection.commit()
                cur = mysql.connection.cursor()
                cur.execute("""
                                       insert into logindata (username,password,role) VALUES (%s, %s, %s)
                                    """, (username, password,role))
                mysql.connection.commit()
                return redirect(url_for('show'))
            else:
                return 'form bhari ne aavo'
        else:
            return 'please login as admin'


@app.route('/cinsert',methods=['POST','GET'])
def cinsert():
    if 'loggedin' in session:
        if session.get('role')=='admin':
            if request.method == 'POST':
                courseid = request.form['courseid']
                faculty = request.form['faculty']
                #print(courseid)
                #role='faculty'
                cur = mysql.connection.cursor()
                cur.execute("""
                       insert into coursedetails (courseid,facultyname) VALUES (%s, %s)
                    """, (courseid,faculty,))
                mysql.connection.commit()

                flash("Data Updated Successfully")

                return redirect(url_for('show'))
            else:
                return 'form bhari ne aavo'
        else:
            return 'please login as admin'

@app.route('/cupdate',methods=['POST','GET'])
def cupdate():
    if 'loggedin' in session:
        if session.get('role')=='admin':
            if request.method == 'POST':
                courseid=request.form['courseid']
                facultyname=request.form['facultyname']
                cur = mysql.connection.cursor()
                cur.execute("""
                                       UPDATE coursedetails
                                       SET  facultyname=%s
                                         
                                       WHERE courseid=%s
                                    """, (facultyname, courseid))
                flash("Data Updated Successfully")
                mysql.connection.commit()
                return redirect(url_for('show'))
            else:
                return 'form bhari ne aavo'
        else:
            return 'please login as admin'




@app.route('/delete/<string:username>', methods=['GET'])
def delete(username):
    if 'loggedin' in session:
        if session.get('role')=='admin':
            flash("Record Has Been Deleted Successfully")
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM studentdetails WHERE username=%s", (username,))
            mysql.connection.commit()
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM logindata WHERE username=%s", (username,))
            mysql.connection.commit()
            os.remove('E:/flask_demo/static/images/'+username+'.jpg')

            return redirect(url_for('show'))
        else:
            return 'form bhari ne aavo'
    else:
        return 'please login as admin'

@app.route('/fdelete/<string:username>', methods=['GET'])
def fdelete(username):
    if 'loggedin' in session:
        if session.get('role')=='admin':
            flash("Record Has Been Deleted Successfully")
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM facultydetails WHERE username=%s", (username,))
            mysql.connection.commit()
            return redirect(url_for('show'))
        else:
            return 'form bhari ne aavo'
    else:
        return 'please login as admin'

@app.route('/cdelete/<string:coursename>', methods=['GET'])
def cdelete(coursename):
    if 'loggedin' in session:
        if session.get('role')=='admin':
            flash("Record Has Been Deleted Successfully")
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM coursedetails WHERE courseid=%s", (coursename,))
            mysql.connection.commit()
            return redirect(url_for('show'))
        else:
            return 'form bhari ne aavo'
    else:
        return 'please login as admin'


@app.route('/resetpassword/<string:username>', methods=['GET'])
def resetpassword(username):
    if 'loggedin' in session:
        if session.get('role')=='admin':
            password='123'
            cur = mysql.connection.cursor()
            cur.execute("""UPDATE logindata
                       SET password=%s
                       WHERE username=%s
                    """, (password, username))
            mysql.connection.commit()
            return redirect(url_for('show'))
        else:
            return 'form bhari ne aavo'
    else:
        return 'please login as admin'

@app.route('/fresetpassword/<string:username>', methods=['GET'])
def fresetpassword(username):
    if 'loggedin' in session:
        if session.get('role')=='admin':
            password='123'
            cur = mysql.connection.cursor()
            cur.execute("""UPDATE logindata
                       SET password=%s
                       WHERE username=%s
                    """, (password, username))
            mysql.connection.commit()
            return redirect(url_for('show'))
        else:
            return 'form bhari ne aavo'
    else:
        return 'please login as admin'

@app.route('/viewattendance',methods=['POST'])
def viewattendance():

    if 'loggedin' in session:

        if session.get('role')=='faculty':
            if request.method == 'POST':
                cid=request.form['cid']
                vdate=request.form['date']
                d1 = datetime.strptime(vdate, '%Y-%m-%d')
                mydate=d1.strftime('%b-%d-%Y')
                global fname
                fname=cid+'_'+mydate+'.csv'
                global myurl
                myurl='http://localhost/attendance/'+fname
                print(myurl)
                req = requests.get(myurl)
                url_content = req.content
                csv_file = open(fname, 'wb')
                print(type(csv_file))
                csv_file.write(url_content)
                csv_file.close()
                return redirect(myurl)

@app.route('/takeattendance', methods=['POST'])
def takeattendance():

    if 'loggedin' in session:

        if session.get('role')=='faculty':
            if request.method == 'POST':
                global courseid
                courseid = request.form['courseid']

                return render_template('index.html')
        else:
            return 'only faculty can take attendance'
@app.route('/camera')
def camera():
    return render_template('camera.html')
def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
    mimetype='multipart/x-mixed-replace; boundary=frame')