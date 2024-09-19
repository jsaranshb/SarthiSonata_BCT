from django.urls import path, include
from .views import *

app_name = 'user'

urlpatterns = [
    path('', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
]
