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
    data = get_user_data()
    doc_ref = fs.collection(u'member').document(u'profiles').collection(u'data')

    doc = doc_ref.document(data['email'])
	
    result = doc.get().to_dict()
    return render(request, "editProfile.html", result)

def editProfileView(request):

    username = request.POST.get('username')
    lurl = request.POST.get('lurl')
    bio = request.POST.get('bio')
    company = request.POST.get('company')
    current_user = get_user_data()
    email = current_user['email']
    
    print(company)
    input = fs.collection(u'member').document(u'profiles').collection(u'data')
    input.document(u'{}'.format(email)).update({
		'company':company,
		'linkedinUrl':lurl,
	})
    doc_ref = fs.collection(u'member').document(u'profiles').collection(u'data')

    doc = doc_ref.document(current_user['email'])
	
    result = doc.get().to_dict()

 
    return render(request, "profile.html", result)