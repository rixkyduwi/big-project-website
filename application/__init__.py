from flask import Flask
from flask_mysqldb import MySQL 
from flask_cors import CORS
import numpy
import tflearn
import tensorflow
import nltk,pickle,json,random;#nltk.download('popular')
nltk.download('punkt')
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
intents = json.loads(open('application/content.json').read())
# words = pickle.load(open('texts.pkl','rb'))
classes = pickle.load(open('labels.pkl','rb'))
mysql = MySQL()
UPLOAD_FOLDER = 'application/static/upload/'
app = Flask(__name__)
# app.config['SECRET_KEY'] = 'secret-key-goes-here'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= True
# app.config['MYSQL_DATABASE_HOST']= 'us-mm-auto-dca-05-a.cleardb.net'
# app.config['MYSQL_DATABASE_USER'] = 'bccc1e5d68a972'
# app.config['MYSQL_DATABASE_PASSWORD']  = '29f342a476deb48'
# app.config['MYSQL_DATABASE_DB'] = 'heroku_068afdbbc88db22'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config.update(dict(
SECRET_KEY="powerful secretkey",
WTF_CSRF_SECRET_KEY="dudu rohosio"
    ))
CORS(app)
try:
  with open("data.pickle", "rb") as f:
    words, labels, training, output = pickle.load(f)
except:
  words = []
  labels = []
  docs_x = []
  docs_y = []

data = json.loads(open('application/content.json').read())
with open("data.pickle", "wb") as f:
    pickle.dump((words, labels, training, output), f)
net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)
model.load('model.tflearn')
def bag_of_words(s, words):
  bag = [0 for _ in range(len(words))]
  s_words = nltk.word_tokenize(s)
  s_words = [stemmer.stem(word.lower()) for word in s_words]

  for se in s_words:
    for i, w in enumerate(words):
      if w == se:
        bag[i] = 1

  return numpy.array(bag)

def chat(msg):
    results = model.predict([bag_of_words(msg, words)])
    results_index = numpy.argmax(results)
    tag = labels[results_index]
    print(tag)
    for tg in data["intents"]:
      if tg['tag'] == tag:
        responses = tg['responses']
        return random.choice(responses)
    print(tag)
    print(random.choice(responses))
    return random.choice(responses)

