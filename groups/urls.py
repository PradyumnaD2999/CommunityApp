from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^groupsView/', views.groupsView, name='groupsView'),
    url(r'^createPost/', views.createPost, name='createPost'),
    url(r'^submitPost/', views.submitPost, name='submitPost'),
    # url(r'^fetchPost/', views.fetchPost, name='fetchPost'),


]