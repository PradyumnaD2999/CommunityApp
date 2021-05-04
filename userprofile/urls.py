from django.urls import path
from django.conf.urls import url
#from .views import UserProfileView
from . import views

urlpatterns = [
    #path('', UserProfileView.as_view(), name='Profile'),
    url(r'^profile/', views.ProfileRedirect, name='Profile'),

]