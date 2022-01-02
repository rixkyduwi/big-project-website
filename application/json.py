from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
import json


# This class tells Python how to turn a Delivery object into a JSON string. 
# This class could encode various types of objects - use isinstance to check what type of thing it is, and return the appropriate JSON
# https://docs.python.org/3/library/json.html

class DeliveryEncoder(json.JSONEncoder):
	def default(self, obj):
		
		if isinstance(obj, Delivery):
			return { 'to' : obj.to,  'from' : obj.fr }

		return json.JSONEncoder.default(self, obj) # default, if not Delivery object. Caller's problem if this is not serialziable.


app = Flask(__name__)

# Tell your app object which encoder to use to create JSON from objects. 
# TODO - what if there are different classes which will be encoded in different ways? 
# http://flask.pocoo.org/snippets/119/
app.json_encoder = DeliveryEncoder


# Example object to represent a model from the database
class Delivery:
	def __init__(self, to, fr):
		self.to = to
		self.fr = fr


# An example API call
@app.route('/api')
def get_json():

	d1 = Delivery('mpls', 'st paul')
	d2 = Delivery('roseville', 'mpls')

	# Pretend this list is the results of a database query
	l = [d1, d2]
 
	return jsonify( l )    # This turns the list of delivery objects into JSON
  
'''
  Output looks like this
  
  [
  {
    "from": "st paul", 
    "to": "mpls"
  }, 
  {
    "from": "mpls", 
    "to": "roseville"
  }
]
  
'''





if __name__ == "__main__":
	app.run()