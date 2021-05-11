from django.urls import path
from django.conf.urls import url
from .views import LoginPageView
from . import views

urlpatterns = [
    path('', LoginPageView.as_view(), name='home'),
	url(r'^loginAuth/', views.loginAuth, name='login'),
    url(r'^registrationRedirect/', views.registrationRedirect, name='register'),
    url(r'^user_registration/', views.user_registration, name='reg_data'),
    url(r'^profile/', views.ProfileRedirect, name='Profile'),
    #path('profile', views.ProfileRedirect, name='Profile'),
    url(r'^Dashboard/', views.DashboardView, name='Dashboard'),
]
