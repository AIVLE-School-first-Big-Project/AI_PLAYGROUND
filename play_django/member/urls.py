from django.urls import path
from . import views

app_name = 'member'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('find_user/', views.find_user, name='find_user'),
    path('update_user/', views.update_user, name='update_user'),
    path('delete_user/', views.delete_user, name='delete_user'),
    path('login/', views.login, name='login'),
    path('refresh_jwt/', views.refresh_jwt, name='refresh_jwt'),
    path('logout/', views.logout, name='logout'),
]
