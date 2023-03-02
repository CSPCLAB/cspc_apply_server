from django.contrib import admin
from apply.models import *
from user.models import *
import csv
from django.http import HttpResponse
from django.db.models import Count
import datetime

from django.shortcuts import get_object_or_404



@admin.action(description='csv 파일 다운로드')
def get_all_resume(self, request, queryset):
    meta = self.model._meta
    field_names = [field.name for field in meta.fields]

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(
        meta)
    writer = csv.writer(response)

    writer.writerow(field_names)
    for obj in queryset:
        row = writer.writerow([getattr(obj, field) for field in field_names])

    return response

#TODO 
@admin.action(description='면접 시간 자동 배치')
def set_interview_time(self, request, queryset): #self = resume model , queryset = 체크했던 object들
    times = [queryset.time for queryset in InterviewTime.objects.all()]
    meta = self.model._meta

    q = Resume.objects.annotate(c=Count('interview_time_choice')).order_by('c')

    for i in q:
        for j in i.interview_time_choice.all():
            if j.time in times :
                time_num = 0
                s = Resume.objects.annotate()
                for _resume in s: #resume에 대해 call하는 부분 문제 어떤방식으로 call해야하나?
                    if j.time==_resume.fixed_interview_time: time_num = time_num + 1
                if time_num==1:
                    plus20 = j.time + datetime.timedelta(minutes=20)
                    a = Resume.objects.annotate()
                    for Res in a:
                        if plus20 == Res.fixed_interview_time: time_num = time_num + 1
                    if time_num == 2: #2개 있을 때
                        i.fixed_interview_time = plus20 + datetime.timedelta(minutes=20)
                        i.save()
                        j.is_fixed = True
                        j.save()
                        times.remove(j.time)
                        break
                    
                    else: #1개 있을
                        i.fixed_interview_time = plus20
                        i.save()
                        break
                
                else: # 0개일때
                    i.fixed_interview_time = j.time
                    i.save()
                    break

@admin.action(description="면접 장소 일괄 지정")
def set_interview_place(self,request,queryset):
    place = get_object_or_404(InterviewPlace)
    for query in queryset:
        query.interview_place = place
        query.save()

@admin.action(description="일괄 서류 불합격")
def set_doc_fail(self,request,queryset):
    for _resume in queryset:
        _resume.is_pass_document = False
        _resume.save()

@admin.action(description="일괄 서류 합격")
def set_doc_pass(self,request,queryset):
    for _resume in queryset:
        _resume.is_pass_document = True
        _resume.save()

@admin.action(description="일괄 최종 합격")
def set_final_pass(self,request,queryset):
    for _resume in queryset:
        _resume.is_pass_final = True
        _resume.save()

@admin.action(description="일괄 최종 불합격")
def set_final_fail(self,request,queryset):
    for _resume in queryset:
        _resume.is_pass_final = False
        _resume.save()

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('applicant', 'name', 'semester',
                    'phone', 'fixed_interview_time')
    search_fields = ['name','applicant__student_id','introduce','motivate']
    actions=[get_all_resume,set_interview_time,set_interview_place,set_doc_fail,set_doc_pass,set_final_pass,set_final_fail]


    def get_ordering(self, request):
        return ['fixed_interview_time']



admin.site.register(InterviewPlace)
admin.site.register(Recruitment)
admin.site.register(InterviewTime)

# Register your models here.
