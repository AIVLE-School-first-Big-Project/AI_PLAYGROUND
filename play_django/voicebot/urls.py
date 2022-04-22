from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:room_name>/', views.room, name='room'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)