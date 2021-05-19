from django.shortcuts import render
from django.contrib import auth
from django.views.generic import TemplateView
from firebase_admin import credentials,firestore,db,auth
import firebase_admin
import pyrebase
from django.contrib.auth.decorators import login_required
from .models import Profile1
import random
from django.contrib.auth import get_user_model
from loginpage.views import get_user_data



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

def editProfile(request):
    res = get_user_data()
    return render(request, "editProfile.html", res)

def editProfileView(request):

    username = request.POST['username']
    lurl = request.POST['lurl']
    bio = request.POST['bio']
    company = request.POST['company']
    res = get_user_data()
    email = res['email']
    
    print(company)
    input = fs.collection(u'member').document(u'profiles').collection(u'data')
    input.document(u'{}'.format(email)).update({
        'username': username,
		'company':company,
		'linkedinUrl':lurl,
        'bio': bio,
	})
 
    return render(request, "profile.html", res)

def changeProfilePicture(request):
    # picture = forms.ImageFields()
    profilePic = request.FILES['profilePic']
    print(profilePic)
    res = get_user_data()
    res['profilePic'] = profilePic
    email = res['email']

    input = fs.collection(u'member').document(u'profiles').collection(u'data')
    input.document(u'{}'.format(email)).update({
        'profilePic': profilePic,
	})

    return render(request, "profile.html", res)

def searchUserview(request):
    res = get_user_data()
    return render(request, "search.html",res)

def searchUser(request):
    res = get_user_data()
    	
    search_Str = request.POST['search_Str'] 

    res['str'] = search_Str
    input = fs.collection(u'member').document(u'profiles').collection(u'data')
    

    return render(request, "search.html",res)