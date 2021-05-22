from django.shortcuts import render
from django.contrib import auth
from django.views.generic import TemplateView
from firebase_admin import credentials,firestore,db,auth
import firebase_admin
import pyrebase
from django.contrib.auth.decorators import login_required
from .models import Profile, FriendRequest
import random
from django.contrib.auth import get_user_model

#import cv2 
import os,argparse 
#import pytesseract ,re
from PIL import Image 
import csv
#import pandas as pd
# Create your views here.

User = get_user_model()


class LoginPageView(TemplateView):
	template_name = 'registration/login.html'

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

cwd = os.getcwd()
cred = credentials.Certificate(os.path.join(cwd, 'wbca-mmcoe2021-firebase-adminsdk-4mnlv-e359f7b1aa.json'))
firebase_admin.initialize_app(cred, {'databaseURL': "https://wbca-mmcoe2021-default-rtdb.firebaseio.com"})
fs = firestore.client()


# Create your views here

global res
res = {}
def loginAuth(request):
	if request.method == "POST":

		email=request.POST.get('email')
		passw = request.POST.get("pass")
		userType = request.POST.get("usertype")
		print(userType)
		if not fs.collection(u'member').document(u'LoginID').collection(u'UniqueID').document(u'{}'.format(email)).get().exists:
			msg = "Please enter valid credentials"
			return render(request,"registration/login.html",{"messg":msg})
		try:
			user = authe.sign_in_with_email_and_password(email,passw)
		except:
			message="invalid credentials"
			return render(request,"registration/login.html",{"messg":message})
		
		session_id=user['idToken']
		request.session['uid']=str(session_id)
		idtoken=request.session.get('uid',None)
		

		currentuser = authe.current_user

		email = currentuser['email']
		print(currentuser['email'])
		
	
	res = fetchPost()
	return render(request, "dashboard.html",res)

def registrationRedirect(request):
    return render(request, "registration/registration.html")


def user_registration(request):
	if request.method == "POST":

		email=request.POST.get('email')
		fname=request.POST.get('firstname')
		mname=request.POST.get('middlename')
		lname=request.POST.get('lastname')
		contact=request.POST.get('contact')
		grad=request.POST.get('graduation')
		branch=request.POST.get('branch')
		company=request.POST.get('company')
		idproof=request.POST.get('idproof')
		lurl=request.POST.get('linkedinurl')
		pw1=request.POST.get('password1')
		pw2=request.POST.get('password2')

		name = fname+' '+lname 
		#print(name)
		colunms = ['username','password','firstname','lastname','email','institution','department']

		#path = "/home/neha/Downloads/BEMOODLE.csv"
		#df = pd.read_csv(path, names=colunms)
		#print(df.head())

		# for i in df['lastname']:
		# 	if i == name:
		# 		print('found')


		if fs.collection(u'member').document(u'LoginID').collection(u'UniqueID').document(u'{}'.format(email)).get().exists:
			msg = "This e-mail is already associated with another account!"
			return render(request,"registration/login.html",{"messg":msg})
		elif fs.collection(u'superadmin').document(u'registration').collection(u'member').document(u'{}'.format(email)).get().exists:
			msg = "Registered with this e-mail,verification pending."
			return render(request,"registration/login.html",{"messg":msg})

		#add to superadmin db for profile verification
		#reg=fs.collection(u'superadmin').document(u'registration').collection(u'member')
	
		authe.create_user_with_email_and_password(email, pw1)
		reg = fs.collection(u'member').document(u'LoginID').collection(u'UniqueID')
		reg.document(u'{}'.format(email)).set({
			'password':pw1
		})
	
		data = fs.collection(u'member').document(u'profiles').collection(u'data')
		data.document(u'{}'.format(email)).set({
			'firstName': fname,
			'middleName':mname,
			'lastName':lname,
			'email':email,
			'contact':contact,
			'graduation':grad,
			'branch':branch,
			'company':company,
			'idProof':idproof,
			'linkedinUrl':lurl,
			'username': fname + lname,
			'userType': 'member',
		})
		
		#Code to check the data from IDproof
		'''
		images=cv2.imread(idproof) 
		gray=cv2.cvtColor(images, cv2.COLOR_BGR2GRAY) 
		#memory usage with image i.e. adding image to memory 
		#filename = "{}.jpg".format(os.getpid()) 
		#cv2.imwrite(filename, gray) 
		text = pytesseract.image_to_string(gray)
		f= open("out.txt","w+")
		f.write(text)
		f.close()
		name_list = []

		with open ('out.txt', 'rt') as myfile:
			for myline in myfile:
				name_list.append(myline)
		for item in name_list:
			if name == item :
				print('Found on ID proof!')
	'''
	return render(request, "registration/login.html")


def ProfileRedirect(request):
	
	res = get_user_data()
	return render(request, "profile.html",res)


def get_user_data():
	currentuser = authe.current_user
	email = currentuser['email']	
	doc_ref = fs.collection(u'member').document(u'profiles').collection(u'data')
	doc = doc_ref.document(currentuser['email'])	
	result = doc.get().to_dict()
	return result

def fetchPost():
    res = get_user_data()
    post_data = fs.collection(u'member').document(u'posts').collection(u'pending')
        
    posts = post_data.document('24WH792WG9')
    post1 = posts.get().to_dict()        
    print(post1['owner'])
    res['description'] = post1['description']
    res['owner'] = post1['owner']
    res['date'] = post1['date']

    return res

def DashboardView(request):
	
	res = fetchPost()
	return render(request, "dashboard.html", res)

