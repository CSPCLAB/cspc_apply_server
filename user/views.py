from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from user.models import Applicant , LabMaster
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate
from user.serializers import LabMasterSerializer, ApplicantSerializer
from drf_yasg.utils import swagger_auto_schema
from swagger_response import *

@swagger_auto_schema(request_body=ApplicantSerializer, method='post', responses=check_id_response)
@api_view(['POST'])
def check_applicant(request):
    try:
        #request에서 이름, 패스워드 추출
        student_id = request.data['student_id']
        password = request.data['password']


        user = authenticate(username=student_id,password=password)
        if user is None:

        # 기존 지원자 로그인 성공
            if Applicant.objects.filter(student_id=student_id):
                return Response(status=500)
            # 새로운 지원자
            else:
                recruit = Recruitment.objects.get()
                print(recruit.process)
                if recruit.process != 'apply':
                    return Response(status=405)
                applicant = Applicant.object.create_user(student_id=student_id,password=password)
                return Response(applicant.id,status=200)
        
        return Response(user.id,status=201)
    # request에서 이름, 패스워드 추출 실패 시
    except AttributeError: 
        return Response(status=404)
    



@swagger_auto_schema(responses=get_master_info_response, method='get')
@api_view(['GET'])
def get_master_info(request):
    master =  get_object_or_404(LabMaster,is_active = True)
    master_serializer = LabMasterSerializer(master)
    return Response(master_serializer.data,status=200)
# Create your views here.
