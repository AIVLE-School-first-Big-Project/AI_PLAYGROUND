from django.urls import path
from . import views

app_name = 'board'

urlpatterns = [
    path('write/', views.write, name = 'write'),
    path('list/', views.list, name='list'),
    path('delete/<int:id>/', views.delete, name = 'delete'),
    path('update/<int:id>/', views.update, name = 'update'),
    path('details/', views.details, name='details'),
    path('download/<int:id>/', views.download, name='download'),
    path('boardcreate/', views.boardcreate, name='boardcreate'),
]