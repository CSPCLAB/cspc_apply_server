from rest_framework.response import Response
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from apply.models import Recruitment
from apply.serializers import *
from swagger_response import *


from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated


# TODO
@swagger_auto_schema(method="get", responses=get_recuit_session_response)
@api_view(["GET"])
def get_recuit_session(request):
    session = Recruitment.objects.order_by("-year", "-term").first()
    if not session:
        return Response({"detail": "진행 중인 모집이 없습니다."}, status=404)

    session.check_process()
    serializer = RecruitSerializer(session)
    return Response(serializer.data, status=200)



class ResumeAPI(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(Resume, applicant=self.request.user)

    @swagger_auto_schema(responses=get_resume_response)
    def get(self, request):
        resume = self.get_object()
        serializer = ResumeSerializer(resume)
        return Response(serializer.data, status=200)

    @swagger_auto_schema(request_body=ResumeRequestSerializer)
    def post(self, request):
        request.data["applicant"] = request.user.id
        serializer = ResumeSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201) 
        return Response(serializer.errors, status=400)

    @swagger_auto_schema(request_body=ResumeSerializer)
    def patch(self, request):
        resume = self.get_object()
        serializer = ResumeSerializer(resume, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)



@swagger_auto_schema(method="get", responses=get_interview_response)
@api_view(["GET"])
def get_interview_time_list(request):
    times = InterviewTime.objects.all().order_by("time") 
    serializer = InterviewtimeSerializer(times, many=True)
    return Response(serializer.data, status=200)


@swagger_auto_schema(method="get", responses=get_result_response)
@permission_classes([IsAuthenticated])
@authentication_classes([BasicAuthentication])
@api_view(["GET"])
def get_result(request):
    resume = get_object_or_404(Resume, applicant=request.user)
    serializer = ResultSerializer(resume)
    return Response(serializer.data, status=200)

