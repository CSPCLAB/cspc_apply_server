from django.urls import path
from user.views import check_applicant, get_master_info

urlpatterns = [
    path("check-id/", check_applicant, name="check_applicant"),
    path("master/", get_master_info, name="get_master_info"),
]
