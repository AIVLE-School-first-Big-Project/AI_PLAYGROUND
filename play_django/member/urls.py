from django.urls import path
from . import views

app_name = 'member'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('refresh_jwt/', views.refresh_jwt, name='refresh_jwt'),
    path('logout/', views.logout, name='logout'),
]
