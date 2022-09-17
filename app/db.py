import json
import firebase_admin
from firebase_admin import db, firestore

cred_obj = firebase_admin.credentials.Certificate('toilet-1c321-firebase-adminsdk-iojrg-a2d280fac3.json')
default_app = firebase_admin.initialize_app(cred_obj, {
    'databaseURL': "https://toilet-1c321-default-rtdb.firebaseio.com/"
})

ref = db.reference("/OverallDB/")

# API call to get all the data in a list
def random():
    """Get all data from the db
    """
    return ref.get()


def get_all_db():
    """Return a json of the db
    """
    stud_json = json.dumps(random(), indent=2, sort_keys=True)
    return stud_json


# define Python user-defined exceptions
class Error(Exception):
    """Base class for other exceptions"""
    pass


class IncompleteTaskError(Error):
    """Raised when there is no description in the task"""


def set_to_db(j_file):
    """Set a new observation to the db
    """
    data = json.loads(j_file)



    if "taskName" and "id" not in data:
        raise IncompleteTaskError
    elif "Deadline" not in data:
        data["Deadline"] = ""
        json_object = json.dumps(data, indent=2, sort_keys=True)
        ref.set(json_object)
    elif "description" not in data:
        data["description"] = ""
        json_object = json.dumps(data, indent=2, sort_keys=True)
        ref.set(json_object)

    ref.push(j_file)

def remove_entry(title):
    records = json.loads(get_all_db())
    if isinstance(records, str):
        records = {"0": records}
    t = list(records.values())
    for i in t:
        if json.loads(i)["taskName"] == title:
            return i
def remove_entry2(j_file):
    """Remove an entry from the database.
    """
    records = json.loads(get_all_db())
    if isinstance(records, str):
        records = {"0": records}
    t = list(records.values())
    accumulator = 0
    for i in t:
        if json.loads(i)["taskName"] == j_file:
            if accumulator == 0:
                ref.set(i)
                accumulator += 1
            else:
                ref.push(i)
