from rest_framework import serializers

from user.models import LabMaster, Applicant

class LabMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabMaster
        fields = ('name','email','phone')

class ApplicantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        fields = ('student_id','password')