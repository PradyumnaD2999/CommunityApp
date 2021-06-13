from loginpage.views import get_user_data, fetchPost
from django.shortcuts import render
import pyrebase
from django.contrib import auth
from firebase_admin import credentials,firestore,db,auth
import firebase_admin
import random
import string
import datetime
from django.core.files.storage import FileSystemStorage
import os

config = {
	'apiKey': "AIzaSyD-THXuPuvdtXFMBvy1-PJo-ueMWu0SJ-E",
	'authDomain': "wbca-mmcoe2021.firebaseapp.com",
  	'projectId': "wbca-mmcoe2021",
	'databaseURL': "https://wbca-mmcoe2021-default-rtdb.firebaseio.com",
  	'storageBucket': "wbca-mmcoe2021.appspot.com",
  	'messagingSenderId': "210306099976",
  	'appId': "1:210306099976:web:c35649974e76992848dabd",
  	'measurementId': "G-RC62WM6F3N"
}

firebase = pyrebase.initialize_app(config)
authe = firebase.auth()

fs = firestore.client()

def randomID():
    S = 10  # number of characters in the string.  
    ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S))    
    print("The randomly generated string is : " + str(ran)) 
    return str(ran)

def groupsView(request):
    return render(request, "groups.html")


def createPost(request):
    if request.method == "POST":
        dateTime = request.POST.get('datetime')
        post_data = fs.collection(u'member').document(u'posts').collection(u'pending')
        # postData = post_data.document(u'M1D5JOI0ZN').get().to_dict()
        postData = post_data.where(u'date', u'==', dateTime).limit(1).stream()
        postData1 = None

        for pd in postData:
            postData1 = pd.to_dict()
            pd.reference.delete()

        postID = randomID()
        postDataUser = fs.collection(u'member').document(u'posts').collection(u'feed')
        postDataUser.document(u'{}'.format(postID)).set({
            'description': postData1['description'],
            'owner': postData1['owner'],
            'date': datetime.datetime.now().strftime("%b %d, %Y at %H:%M"),
            'timestamp': datetime.datetime.now().strftime("%Y%m%d%H%M%S%f"),
            'imgpostUrl' : postData1['imgpostUrl']
        })

    res = fetchPost()        
    return render(request, "dashboard.html", res)

def submitPost(request):
    res = fetchPost()
    if request.method == "POST":
        postimg = request.FILES['postimg'] if 'postimg' in request.FILES else None
        desc = request.POST.get('desc')

        fname = postimg.name
        print(fname)
        f = FileSystemStorage()
        file = f.save(fname, postimg)
        fileurl = f.url(file)
        owner = res['firstName'] + res['lastName']
        postID = randomID()

        post_data = fs.collection(u'member').document(u'posts').collection(u'pending')
        post_data.document(u'{}'.format(postID)).set({
            'owner': owner,
            'description' : desc,
            'date': datetime.datetime.now().strftime("%b %d, %Y at %H:%M:%S #%f"),
            'default': False,
            'timestamp': datetime.datetime.now().strftime("%Y%m%d%H%M%S%f"),
            'imgpostUrl' : fileurl,
        })

        # post_data.document(u'M1D5JOI0ZN').update({
        #     'description': desc,
        #     'owner': owner,
        #     'date': datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
        # })

    return render(request, "dashboard.html", res)
