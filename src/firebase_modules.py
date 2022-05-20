import pyrebase

firebase = None
storage = None


config = {
    "apiKey": "AIzaSyBqlCGdqvx-yefYo8hywI5uIahH60H8oU0",
    "authDomain": "fingerprint-contact.firebaseapp.com",
    "databaseURL": "",
    "projectId": "fingerprint-contact",
    "storageBucket": "fingerprint-contact.appspot.com",
    "serviceAccount": "/home/pi/Fingerprint_Contact_Tracing/webapp/database/serviceAccountKey.json",
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()


def upload_to_firebase(path_on_cloud, path_local):
    
    
    storage.child(path_on_cloud).put(path_local)


def download_from_firebase(path_on_cloud, path_local):
    
    
    storage.child(path_on_cloud).download(path_local)


