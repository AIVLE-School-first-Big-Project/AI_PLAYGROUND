from django.urls import path, include
from . import views
from .views import *

from django.conf import settings 
from django.conf.urls.static import static

app_name = 'pcolor'
urlpatterns = [
    path('', views.fileUpload , name='pcimgupload'),
    path('save/', views.save, name="save"),

    # path('pcresult/', views.pcresult, name='pcresult'),
]