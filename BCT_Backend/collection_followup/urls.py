from django.urls import path
from .views import *

urlpatterns = [
    path('', CollectionFollowUp.as_view(), name='collection_followup'),
    path('calling_bucket/<int:id>/', CallingBucket.as_view(), name='calling_bucket'),
    path('todays_promises/', TodaysPromises.as_view(), name='todays_promises'),
]
