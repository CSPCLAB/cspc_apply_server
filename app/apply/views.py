from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.views import APIView
from django.http import Http404
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from apply.models import Recruitment
from apply.serializers import *
from swagger_response import *


from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

#TODO
@swagger_auto_schema(method="get",responses=get_recuit_session_response)
@api_view(['GET'])
def get_recuit_session(request):
    session = get_object_or_404(Recruitment)
    session.check_process()
    serializer = RecruitSerializer(session)
    return Response(serializer.data, status=200)

class ResumeAPI(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self,applicant):
        
        return get_object_or_404(Resume,applicant=applicant)
       
        
    @swagger_auto_schema(responses=get_resume_response,authentication_classes=[BasicAuthentication])
    def get(self,request):
        if request.user.is_authenticated:
            resume = self.get_object(request.user)
            serializer = ResumeSerializer(resume)
            return Response(serializer.data, status=200)
        else:
            return Response(status=401)
    
    @swagger_auto_schema(request_body=ResumeRequestSerializer,authentication_classes=[BasicAuthentication])
    def post(self,request):
        if request.user.is_authenticated:
            request.data['applicant'] = request.user.id
            serializer = ResumeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=200)
            else:
                return Response(serializer.errors,status=400) #지원서 수정하는데 잘못 save되면 응답 & status #
        else:
            return Response(status=401)

    @swagger_auto_schema(request_body=ResumeSerializer,authentication_classes=[BasicAuthentication])
    def patch(self,request):
        if request.user.is_authenticated:
            resume = self.get_object(request.user)
            serializer = ResumeSerializer(resume, data=request.data, partial=True)
            #print(request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=200)
            else:
                return Response(serializer.errors,status=400) #지원서 수정하는데 잘못 save되면 응답 & status #
        else:
            return Response(stauts=401)

@swagger_auto_schema(method="get", responses=get_interview_response)
@api_view(['GET'])
def get_interview_time_list(reqeust):
    times = InterviewTime.objects.all().order_by('time')
    serializer = InterviewtimeSerializer(times,many=True)
    return Response(serializer.data,status=200)


@swagger_auto_schema(method="get", responses=get_result_response, authentication_classes=[BasicAuthentication])
@permission_classes([IsAuthenticated])
@authentication_classes([BasicAuthentication])
@api_view(['GET'])
def get_result(request):
    if request.user.is_authenticated:
        resume = get_object_or_404(Resume,applicant=request.user)
        serializer = ResultSerializer(resume)
        return Response(serializer.data,status=200)
    else:
        return Response(status=401)