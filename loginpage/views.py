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
from django.core.mail import send_mail
import smtplib, ssl
from django.core.files.storage import FileSystemStorage
import os,argparse
from firebase_admin import auth
# import cv2 
# import pytesseract ,re
# from PIL import Image 
# import csv
# import pandas as pd

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

global res
res = {}

def loginAuth(request):
	if request.method == "POST":
		email=request.POST.get('email')
		passw = request.POST.get("pass")
		userType = request.POST.get("usertype")
		print(userType)

		if not fs.collection(u'member').document(u'profiles').collection(u'data').document(u'{}'.format(email)).get().exists:
			msg = "Please Enter Valid Credentials"
			return render(request,"registration/login.html",{"messg":msg})
		elif fs.collection(u'member').document(u'profiles').collection(u'data').document(u'{}'.format(email)).get().to_dict()['userType'] != userType:
			msg = "User Type Not Valid"
			return render(request,"registration/login.html",{"messg":msg})

		try:
			user = authe.sign_in_with_email_and_password(email,passw)
		except:
			message="Invalid Credentials"
			return render(request,"registration/login.html",{"messg":message})

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
		idproof = request.POST.get('idproof')
		lurl=request.POST.get('linkedinurl')
		pw1=request.POST.get('password1')
		pw2=request.POST.get('password2')

		name = fname+' '+lname 

		if fs.collection(u'member').document(u'profiles').collection(u'data').document(u'{}'.format(email)).get().exists:
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
		subject = "Registration Successful!"
		text = "Thank You For registering to WB Community."
		sendemail(email,subject,text)

		#Code to check the data from IDproof
	
		# images=cv2.imread(idproof) 
		# gray=cv2.cvtColor(images, cv2.COLOR_BGR2GRAY) 
		# #memory usage with image i.e. adding image to memory 
		# #filename1 = "{}.jpg".format(os.getpid()) 
		# #cv2.imwrite(filename1, gray) 
		# text = pytesseract.image_to_string(gray)
		# f1= open("out.txt","w+")
		# f1.write(text)
		# f1.close()
		# name_list = []

		# with open ('out.txt', 'rt') as myfile:
		# 	for myline in myfile:
		# 		name_list.append(myline)
		# for item in name_list:
		# 	if name == item :
		# 		print('Found on ID proof!')
	
	return render(request, "registration/login.html")

def sendemail(emailID,subject,text):
	port = 587  # For starttls
	smtp_server = "smtp.gmail.com"
	sender_email = "wbcommunityapp@gmail.com"
	receiver_email = emailID
	password = 'mmcoe2021@BEProject'
	message = 'Subject: {}\n\n{}'.format(subject, text)
	context = ssl.create_default_context()
	with smtplib.SMTP(smtp_server, port) as server:
		server.ehlo()
		server.starttls(context=context)
		server.ehlo()
		server.login(sender_email, password)
		server.sendmail(sender_email, receiver_email, message)
		server.quit()
	

def resetPasswordredirect(request):
	return render(request, "resetPassword.html")


def resetPassword(request):
	if request.method == 'POST':
		emailID = request.POST.get('email')

		# send_mail(
		#     'No-reply: Reset Passsword link',
		#     'Click on the below link to reset your password and login again',
		#     'wbcommunityapp@gmail.com',
		#     [emailID],
		#     fail_silently=False,
		# )
		# port = 587  # For starttls
		# smtp_server = "smtp.gmail.com"
		# sender_email = "wbcommunityapp@gmail.com"
		# receiver_email = emailID
		# password = 'mmcoe2021@BEProject'
		
		# Subject = "Password Reset Link"
		# Text = "Click on the link below to reset your password.\n http://127.0.0.1:8000/setPasswordredirect"
		# message = 'Subject: {}\n\n{}'.format(Subject, Text)

		# context = ssl.create_default_context()
		# with smtplib.SMTP(smtp_server, port) as server:
		# 	server.ehlo()
		# 	server.starttls(context=context)
		# 	server.ehlo()
		# 	server.login(sender_email, password)
		# 	server.sendmail(sender_email, receiver_email, message)
		# 	server.quit()
	
		authe.send_password_reset_email(emailID)
		msg = "Reset Password link sent to you email address."

	return render(request, "registration/login.html",{"messg":msg})
	
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
	posts = []
	
	memberCount = 0
	member_data = fs.collection(u'member').document(u'profiles').collection(u'data')
	members = member_data.where(u'userType', u'==', 'member').stream()
	for m in members:
		memberCount = memberCount + 1
 
	if res['userType'] == 'admin':
		post_data = fs.collection(u'member').document(u'posts').collection(u'pending')
		postData = post_data.where(u'default', u'==', False).order_by(u'timestamp', direction=firestore.Query.DESCENDING).stream()
		for pd in postData:
			posts.append(pd.to_dict())
    
	elif res['userType'] == 'member':
		post_data = fs.collection(u'member').document(u'posts').collection(u'feed')
		postData = post_data.order_by(u'timestamp', direction=firestore.Query.DESCENDING).stream()
		for pd in postData:
			posts.append(pd.to_dict())

	res['posts'] = posts
	res['memberCount'] = memberCount
	#print(res)
	return res

def DashboardView(request):	
	res = fetchPost()
	return render(request, "dashboard.html", res)
