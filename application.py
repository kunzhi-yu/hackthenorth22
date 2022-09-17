from flask import Flask
from flask import jsonify, request

import firebase_admin
from firebase_admin import db

app = Flask(__name__)

cred_obj = firebase_admin.credentials.Certificate('toilet-1c321-firebase-adminsdk-iojrg-a2d280fac3.json')
default_app = firebase_admin.initialize_app(cred_obj, {
	'databaseURL': "https://toilet-1c321-default-rtdb.firebaseio.com/"
	})
"""
Things to do here":


get the data and shit it out
"""


ref = db.reference("/OverallDB/")
all_data = ref.get()

@app.route("/rando", methods=["GET"])
def random():
	return [all_data]

if __name__ == '__main__':
    app.run(debug=True) 

