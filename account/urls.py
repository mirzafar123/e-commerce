from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('check-user/', check_user_exists, name='check_user'),
    path('profile/', user_profile, name='user_profile')
]
