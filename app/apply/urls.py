from django.contrib import admin
from django.urls import path
from apply.views import *

urlpatterns = [
    path('recruit/', get_recuit_session, name='get_recuit_session'),
    path('resume/', ResumeAPI.as_view(), name='resume_api'),
    path('interview/', get_interview_time_list, name='get_interview_time_list'),
    path('result/', get_result, name='get_result'),
]
