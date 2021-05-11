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

#import cv2 
import os,argparse 
#import pytesseract ,re
from PIL import Image 
import csv
#import pandas as pd
# Create your views here.



def editProfile(request):
    return render(request, "editProfile.html")