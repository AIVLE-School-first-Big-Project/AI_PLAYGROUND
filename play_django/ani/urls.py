from django.urls import path, include
from . import views
from .views import *

from django.conf import settings 
from django.conf.urls.static import static

app_name = 'ani'
urlpatterns = [
    path('', views.fileUpload, name='fileupload'),
]



