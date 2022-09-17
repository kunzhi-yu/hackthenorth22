from flask import Flask

import firebase_admin
from firebase_admin import db

cred_obj = firebase_admin.credentials.Certificate('toilet-1c321-firebase-adminsdk-iojrg-a2d280fac3.json')
default_app = firebase_admin.initialize_app(cred_object, {
	'databaseURL': "https://console.firebase.google.com/u/0/project/toilet-1c321/database/toilet-1c321-default-rtdb/data/~2F/OverallDB"
	})

