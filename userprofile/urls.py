from django.urls import path
from django.conf.urls import url
from .views import editProfile, editProfileView
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    #path('', UserProfileView.as_view(), name='Profile'),
    url(r'^editProfile/', views.editProfile, name='editProfile'),
    url(r'^editProfileView/', views.editProfileView, name='editProfile'),
    url(r'^changeProfilePicture/', views.changeProfilePicture, name='changeProfilePicture'),
    url(r'^searchUserview/', views.searchUserview, name='searchUserview'),
    url(r'^searchUser/', views.searchUser, name='searchUser'),



]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)