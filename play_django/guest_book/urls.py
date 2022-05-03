from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

app_name = 'guest_book'


urlpatterns = [
    path('', views.index, name='guest'),


]+ static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT)