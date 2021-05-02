from django.shortcuts import render
from django.contrib import auth
from django.views.generic import TemplateView
from firebase_admin import credentials,firestore,db,auth
import firebase_admin
import pyrebase
#import cv2 
import os,argparse 
#import pytesseract ,re
from PIL import Image 
import csv
#import pandas as pd
# Create your views here.

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

# Create your views here.
def loginAuth(request):
	email=request.POST.get('email')
	passw = request.POST.get("pass")
	userType = request.POST.get("usertype")
	print(userType)
	if not fs.collection(u'{}'.format(userType)).document(u'LoginID').collection(u'UniqueID').document(u'{}'.format(email)).get().exists:
		msg = "Please enter valid credentials"
		return render(request,"registration/login.html",{"messg":msg})
	try:
		user = authe.sign_in_with_email_and_password(email,passw)
	except:
		message="invalid credentials"
		return render(request,"registration/login.html",{"messg":message})
	print(user['idToken'])
	session_id=user['idToken']
	request.session['uid']=str(session_id)
	return render(request, "dashboard.html",{"e":email})

def registrationRedirect(request):
    return render(request, "registration/registration.html")

name = ''

def user_registration(request):
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
	print(name)
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



#class Profileview(TemplateView):
