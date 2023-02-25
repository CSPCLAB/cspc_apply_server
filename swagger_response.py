from drf_yasg import openapi

from user.serializers import *
from apply.serializers import *

check_id_response = openapi.Responses(
    responses={200: "첫 지원자", 201: "기존 지원자", 500: "로그인 실패", 404: "request data 없음"})

get_master_info_response = openapi.Responses(responses={200: LabMasterSerializer()})


get_recuit_session_response = openapi.Responses(
    responses={200: RecruitSerializer(), 404 : "Not found"}
)

get_resume_response = openapi.Responses(
    responses={200: ResumeRequestSerializer(), 400: "Error"}
)

get_interview_response = openapi.Responses(
    responses={200: InterviewtimeSerializer(many=True), 400: "Error"}
)

get_result_response = openapi.Responses(
    responses={200: ResultSerializer(),404 : "Not found"}
)