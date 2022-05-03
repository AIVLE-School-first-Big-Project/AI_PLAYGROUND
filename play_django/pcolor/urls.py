from django.urls import path, include
from . import views
from .views import *

from django.conf import settings 
from django.conf.urls.static import static

app_name = 'pcolor'
urlpatterns = [
    path('', views.fileUpload , name='pcimgupload'),
    path('save/', views.download , name='download'),
    path('result/', views.share, name='share'),
 # path('pcresult/', views.pcresult, name='pcresult'),
]