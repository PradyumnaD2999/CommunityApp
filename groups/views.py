from loginpage.views import get_user_data
from django.shortcuts import render
import pyrebase
from django.contrib import auth
from firebase_admin import credentials,firestore,db,auth
import firebase_admin
import random
import string



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
# Create your views here.

def randomID():
    S = 10  # number of characters in the string.  
    ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S))    
    print("The randomly generated string is : " + str(ran)) 
    return str(ran)


def groupsView(request):

    return render(request, "groups.html")


def createPost(request):
    res = get_user_data()
    if request.method == "POST":
        post_data = fs.collection(u'member').document(u'posts').collection(u'pending')

        
    return render(request, "dashboard.html")

def submitPost(request):

    res = get_user_data()
    if request.method == "POST":

        desc = request.POST.get('desc')
        owner = res['firstName'] + res['lastName']
        postID = randomID()
        post_data = fs.collection(u'member').document(u'posts').collection(u'pending')
        post_data.document(u'{}'.format(postID)).set({
            'description': desc,
            'owner': owner,
        })

    
    return render(request, "dashboard.html")    

def fetchPost(request):
    res = get_user_data()
    if request.method == "GET":
        post_data = fs.collection(u'member').document(u'posts').collection(u'pending')
        
        posts = post_data.document('default')
        post1 = posts.get().to_dict()        
        print(post1['owner'])
        
    return render(request, "dashboard.html", res)
