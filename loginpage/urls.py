from django.urls import path
from django.conf.urls import url
from .views import LoginPageView
from . import views

urlpatterns = [
    path('', LoginPageView.as_view(), name='home'),
	url(r'^loginAuth/', views.loginAuth, name='login'),
    url(r'^registrationRedirect/', views.registrationRedirect, name='register'),
]
