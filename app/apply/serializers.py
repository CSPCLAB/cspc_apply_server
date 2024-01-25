from rest_framework import serializers
from apply.models import *
from user.serializers import *
class RecruitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recruitment
        fields = '__all__'


class InterviewtimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewTime
        fields = '__all__'


class ResumeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Resume
        fields = ['interview_time_choice', 'name', 'semester', 'phone',
                  'introduce', 'motivate', 'to_do', 'etc', 'applicant', 'updated_at']

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('interview_requirement', None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
    # def update(self, instance, validated_data):
    #     nested_serializer = self.fields['interview_time_choice']
    #     nested_instance = instance.interview_time_choice
    #     # note the data is `pop`ed
    #     nested_data = validated_data.pop('interview_time_choice')
    #     nested_serializer.update(nested_instance, nested_data)
    #     # this will not throw an exception,
    #     # as `profile` is not part of `validated_data`
    #     return super(ResumeSerializer, self).update(instance, validated_data)
    
    # def create(self, validated_data):
    #     times = validated_data.pop('interview_time_choice')
    #     print(times)
    #     resume = Resume.objects.create(**validated_data)
    #     for time in times:
    #         print(time)
    #         t = InterviewTime.objects.get(id=time['id'])
    #         resume.interview_time_choice.add(t)
    #     resume.save()
    #     return resume

class ResumeRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ['interview_time_choice', 'name', 'semester', 'phone',
                  'introduce', 'motivate', 'to_do', 'etc', 'interview_requirement']


class ResultSerializer(serializers.ModelSerializer):
    interview_place = serializers.CharField(source='interview_place.place')
    class Meta:
        model = Resume
        fields = ['name','fixed_interview_time','interview_place','is_pass_document','is_pass_final']
