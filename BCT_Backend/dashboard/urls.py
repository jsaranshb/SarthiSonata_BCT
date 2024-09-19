from django.urls import path
from .views import BusinessCallingAPI

app_name = 'dashboard'

urlpatterns = [
    path('business_calling/', BusinessCallingAPI.as_view(), name='business_calling'),
]