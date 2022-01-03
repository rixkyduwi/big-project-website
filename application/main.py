import re
from flask import Blueprint, render_template,request,redirect,url_for,jsonify,make_response,flash
from application import db,app,mysql
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, current_user
from application.models import User
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
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    else:
        return render_template('index.html')
@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('admin/index.html', name=current_user.name)
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
@main.route('/atributuser/<jenis>',methods=['POST'])
def atributuser(jenis):
    warga = mysql.connection.cursor()
    user = request.form['user']
    berat = request.form['berat(KG)']
    warga.execute("INSERT INTO akumulasi (jenis,user,berat) values (%s,%s,%s)",(jenis,user,(berat),))
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
    gambar = request.form['gambar']
    user = request.form['user']
    berat = request.form['berat']
    akumulasi.execute("UPDATE akumulasi SET jenis ='"+ jenis+"',gambar= '" +gambar+"',user='"+ user+"',berat = '"+berat+"' WHERE  id ="+id)
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
@main.route('/admin/latih_chatbot',methods=['GET','POST'])
@login_required
def latih_chatbot():
    if request.method == 'GET':
        #cetak isi json
        tag=[]
        for i in range(len(intents['intents'])):
            tag.append=(f"Tag: {intents['intents'][i]['tag']}")
            tag.append=("Parameter:")
            for j in range(len(intents['intents'][i]['patterns'])):
                print(f"- {intents['intents'][i]['patterns'][j]}")
            print("Respon:")
            print(f"- {intents['intents'][i]['responses']}")
        return render_template('list')
    elif request.method == 'POST':
        #edit&save json
        data = request.json
        return jsonify(data)
@main.route('/admin/listadmin')
@login_required
def listadmin():
    return render_template('admin/listadmin.html', admin = User.query.all().fetchall(),listadmin=True)

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
@main.route('/history/<username>', methods=['POST'])
@login_required
def historyuser(username):
    warga = mysql.connection.cursor()
    warga.execute("SELECT jenis,count(gambar),user FROM akumulasi WHERE user = %s GROUP BY jenis" , (username,))
    history = warga.fetchall()
    return render_template('history.html',history)
