import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("/Users/kaidenmerchant/Desktop/Coding Projects/Home_Security/venv/automated_home_security/resources/serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':'https://facialrecognitionsecurity-default-rtdb.firebaseio.com/'
})

ref = db.reference('People')


#create data in json format
data = {
    '00001':{
        'name':'Elon Musk',
        'Relationship':'friend',
        'Last Appearance':'TIME HERE',
        'Total Appearances':0
    },
    '00002':{
        'name':'Jeff Bezos',
        'Relationship':'Landscaper',
        'Last Appearance':'TIME HERE',
        'Total Appearances':0
    },
    '00003':{
        'name':'Kaiden Merchant',
        'Relationship':'owner',
        'Last Appearance':'TIME HERE',
        'Total Appearances':0
    }
}

#POST data to database
for key,value in data.items():
    ref.child(key).set(value)