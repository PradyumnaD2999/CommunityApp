from django.urls import path
from django.conf.urls import url
from .views import editProfile
from . import views

urlpatterns = [
    #path('', UserProfileView.as_view(), name='Profile'),
    url(r'^editProfile/', views.editProfile, name='editProfile'),

]