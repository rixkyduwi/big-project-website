import re
from flask import Blueprint, render_template,request,redirect,url_for,jsonify,make_response,flash
from application import db,app,mysql
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, current_user
from application.models import User
from application.CRUD import Data
#chatbot
import nltk,pickle,json,random;nltk.download('popular')
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import numpy as np
from json_modify import apply_actions
from keras.models import load_model
model = load_model('model.h5')
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
    return render_template('index.html')
@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('admin/index.html', name=current_user.name)
@main.route('/admin/warga',methods=['GET','POST','PUT','DELETE'])
def warga():
    try:
        dt = Data()
        values = ()
        if request.method == 'GET':
            warga = mysql.connection.cursor()
            warga.execute("SELECT * FROM data_warga")
            data_warga = warga.fetchall()
            warga.close()
            return render_template('admin/data_warga.html',data_warga=data_warga)

        elif request.method == 'POST':
                datainput = request.json
                nama = datainput['nama']
                no_rumah = datainput['no_rumah']
                kontak = datainput['kontak']
                password = datainput['password']
                email = datainput['email']
                query = "INSERT INTO data_warga (nama,no_rumah,kontak,password,email,) values (%s,%s,%s,%s,%s) "
                values = (nama,no_rumah, kontak,password,email)
                dt.insert_data(query, values)  
                data = [{
                    'pesan': 'berhasil menambah data' 
                }]
        
        elif request.method == 'PUT':
            query = "UPDATE data_warga SET id = %s"
            datainput = request.json
            id_ = datainput['id']
            values += (id_,)
            if 'nama' in datainput:
                nama = datainput['nama']
                values += (nama, )
                query += ", nama = %s"
            if 'no_rumah' in datainput:
                pekerjaan = datainput['no_rumah']
                values += (pekerjaan, )
                query += ", no_rumah = %s"
            if 'kontak' in datainput:
                usia = datainput['kontak']
                values += (usia, )
                query += ", usia = %s"
            if 'password' in datainput:
                usia = datainput['password']
                values += (usia, )
                query += ", password = %s"
            if 'email' in datainput:
                usia = datainput['email']
                values += (usia, )
                query += ", email = %s"
            query += " where id = %s"
            values += (id_,)
            dt.insert_data(query, values)
            data =[{
                'pesan' : 'berhasil mengubah data'
            }]

        else:
            print('%s')
            query = "DELETE FROM data_warga where id = %s"
            id_ = request.args.get("id")
            values = (id_,)
            dt.insert_data(query, values)
            data =[{
                'pesan': 'berhasil menghapus'
            }]
    except Exception as e:
        return make_response(jsonify({'error':str(e)}),400)
    return make_response(jsonify({'data':data}),200)
@main.route('/deleteuser/<id>')
def deleteuser(id):
    try:
        dt = Data()
        values = ()
        if request.method == 'GET':
            warga = mysql.connection.cursor()
            warga.execute("DELETE FROM data_warga where id = "+id)
            mysql.connection.commit()
            data_warga = warga.fetchall()
    except Exception as e:
        print(id)
        return render_template('admin/data_warga.html')
    return redirect(url_for('main.warga'))
@main.route('/formupdate/<id>', methods=['GET'])
def formupdate(id):
    warga = mysql.connection.cursor()
    warga.execute("SELECT * FROM data_warga where id ="+id)
    data_warga = warga.fetchall()
    warga.close()
    print(data_warga)
    return render_template('admin/edit_warga.html',data_warga=data_warga)
@main.route('/updateuser/<id>',methods=['POST'])
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
@main.route('/atributuser/<jenis>',methods=['POST'])
def atributuser(jenis):
    warga = mysql.connection.cursor()
    user = request.form['user']
    warga.execute("INSERT INTO uploadgambar (jenis,user) values (%s,%s)",(jenis,user,))
    mysql.connection.commit()
    return "halo"

@main.route('/uploadgambar')
def upload_form():
	return render_template('upload.html')
@main.route('/uploadgambar', methods=['POST'])
def upload_image():
	if 'gambar' not in request.files:
		flash('No file part')
		return redirect(request.url)
	file = request.files['gambar']
	if file.filename == '':
		flash('No image selected for uploading')
		return redirect(request.url)
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		#print('upload_image filename: ' + filename)
		flash('Image successfully uploaded and displayed below')
		return render_template('upload.html', filename=filename)
	else:
		flash('Allowed image types are -> png, jpg, jpeg, gif')
		return redirect(request.url)

@main.route('/display/<filename>')
def display_image(filename):
	#print('display_image filename: ' + filename)
	return redirect(url_for('static', filename='upload/' + filename), code=301)

@main.route('/admin/anorganik')
@login_required
def anorganik():
    warga = mysql.connection.cursor()
    warga.execute("SELECT * FROM uploadgambar WHERE jenis = 'anorganik'")
    data_warga = warga.fetchall()
    warga.close()
    return render_template('admin/anorganik.html', uploadgambar=data_warga,anorganik=True)
@main.route('/admin/organik')
@login_required
def organik():
    warga = mysql.connection.cursor()
    warga.execute("SELECT * FROM uploadgambar WHERE jenis = 'organik'")
    data_warga = warga.fetchall()
    warga.close()
    return render_template('admin/organik.html', uploadgambar=data_warga,organik=True)
@main.route('/admin/b3')
@login_required
def b3():
    warga = mysql.connection.cursor()
    warga.execute("SELECT * FROM uploadgambar WHERE jenis = 'b3'")
    data_warga = warga.fetchall()
    warga.close()
    return render_template('admin/b3.html', uploadgambar=data_warga,b3=True)
@main.route('/admin/latih_chatbot')
@login_required
def latih_chatbot():
    filename = 'application/content.json'
    with open(filename, 'r') as f:
        data = json.load(f)
        data['id'] = 134 # <--- add `id` value.

        os.remove(filename)
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    return jsonify(intents)
@main.route('/admin/listadmin')
@login_required
def listadmin():
    user = User.query().fetchall()
    warga = mysql.connection.cursor()
    warga.execute("SELECT * FROM data_warga")
    data_warga = warga.fetchall()
    warga.close()
    return render_template('admin/listadmin.html', data_warga=data_warga,listadmin=True)

@main.route('/chatbot')
def chatbot():
    return render_template('admin/chatbot.html')
def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word - create short form for word
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words
# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result

def chatbot_response(msg):
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    return res
@main.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return chatbot_response(userText)
@main.route('/getname/<username>', methods=['POST'])
def extract_name(username):
    warga = mysql.connection.cursor()
    password = request.form['password']
    warga.execute("SELECT email FROM data_warga WHERE email= %s AND password = %s" , (username, password,))
    masuk = warga.fetchall()
    return "halo"+str(masuk)
@main.route('/getsampah', methods=['POST'])
def sampah(username):
    warga = mysql.connection.cursor()
    warga.execute("SELECT * FROM uploadgambar WHERE user = " , (username,))
    masuk = warga.fetchall()
    return render_template('user.html',data_warga=masuk)
@main.route('/reguser/<username>', methods=['POST'])
def reguser(username):
    warga = mysql.connection.cursor()
    nama = request.form['nama']
    email = request.form['email']
    password = request.form['password']
    
    no_rumah = request.form['no_rumah']
    kontak = request.form['kontak']
    warga.execute("INSERT INTO data_warga (nama,email,password,no_rumah,kontak) values (%s,%s,%s,%s,%s)",(nama,email,password,no_rumah,kontak,))
    mysql.connection.commit()
    return "halo"+str(nama)

@main.route('/tambahgambar/<gambar>', methods=['POST'])
def tambahgambar(gambar):
    warga = mysql.connection.cursor()
    warga.execute("INSERT INTO tambahgambar (gambar) values (%s)",(gambar,))
    mysql.connection.commit()
    return 'berhasil menambah data'
@main.route('/history/<username>', methods=['POST'])
def historyuser(username):
    warga = mysql.connection.cursor()
    warga.execute("SELECT * FROM uploadgambar WHERE user = %s " , (username,))
    history = warga.fetchall()
    return "halo"+str(history)
