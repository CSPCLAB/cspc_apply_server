from django.contrib import admin
from apply.models import *
from user.models import *
import csv
from django.http import HttpResponse
from django.db.models import Count
import datetime

from django.shortcuts import get_object_or_404


@admin.action(description="csv 파일 다운로드")
def get_all_resume(self, request, queryset):
    meta = self.model._meta
    field_names = [
        "name",
        "applicant",
        "phone",
        "semester",
        "introduce",
        "motivate",
        "to_do",
        "etc",
        "fixed_interview_time",
    ]
    excel_row = [
        "이름",
        "학번",
        "전화번호",
        "학기",
        "자기소개",
        "지원동기",
        "하고 싶은 것",
        "기타",
        "면접 일자",
    ]
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename={}.csv".format(meta)
    writer = csv.writer(response)

    writer.writerow(excel_row)
    for obj in queryset:
        row = writer.writerow([getattr(obj, field) for field in field_names])

    return response


@admin.action(description="면접 시간 자동 배치")
def set_interview_time(
    self, request, queryset
):  # self = resume model , queryset = 체크했던 object들
    # 면접 시간(is_fixed)과 지원자의 면접 시간(fixed_interview_time) 초기화
    InterviewTime.objects.all().update(is_fixed=False)
    Resume.objects.all().update(fixed_interview_time=None)

    # 면접 시간 객체를 datetime 객체로 변환
    interview_times = {
        interview_time.id: interview_time.time
        for interview_time in InterviewTime.objects.all()
    }

    # 면접시간 별 수요도 체크를 위한 딕셔너리
    # 시간당 최대 3명만 배정하기 위해 카운트하는 배열
    time_count = {id: 0 for id in interview_times.keys()}
    fixed_applicant_count = {id: 0 for id in interview_times.keys()}

    # 서류 통과한 사람들에 한해서 면접 시간 배치
    applicants = (
        Resume.objects.filter(is_pass_document=True)
        .annotate(c=Count("interview_time_choice"))
        .order_by("c")
    )

    # 면접 시간 수요도 조사
    for applicant in applicants:
        for choice in applicant.interview_time_choice.all():
            # choice_time = datetime.strptime(choice.time, "%Y/%m/%d %H:%M:%S")
            choice_time = choice.time
            # 선택된 시간이 면접 시간 목록에 있다면 count 증가
            for interview_time_id, interview_time in interview_times.items():
                if choice_time == interview_time:
                    time_count[interview_time_id] += 1

    # 수요도가 낮은 시간부터 배정하기 위해 오름차순 정렬
    sorted_time_counts = (
        InterviewTime.objects.annotate(applicant_count=Count("interview_time"))
        .filter(is_fixed=False)
        .order_by("applicant_count", "time")
    )

    # 각 지원자에게 가장 수요가 적은 면접 시간을 할당
    for interview_time in sorted_time_counts:
        for applicant in applicants:
            if applicant.fixed_interview_time == None:
                # 해당 시간대가 꽉 찼으면 건너뛰기 (이미 3명이 배정됨)
                if fixed_applicant_count[interview_time.id] >= 3:
                    continue

                chosen_times = applicant.interview_time_choice.all()
                for choice in chosen_times:
                    choice_time = choice.time
                    # 선택된 시간이 현재 순회 중인 면접 시간과 같은지 확인
                    if choice_time == interview_time.time and not choice.is_fixed:
                        plus20 = choice_time + timedelta(
                            minutes=20 * fixed_applicant_count[interview_time.id]
                        )
                        # print(plus20)
                        # 지원자에게 면접 시간 할당
                        applicant.fixed_interview_time = plus20
                        applicant.save()

                        # 할당된 시간의 수요를 1 증가시킴
                        fixed_applicant_count[interview_time.id] += 1

                        # 시간대가 꽉 찼으면 is_fixed 속성을 True로 설정
                        if fixed_applicant_count[interview_time.id] == 3:
                            interview_time.is_fixed = True
                            interview_time.save()

                        # break
                else:
                    # 선택한 모든 시간이 이미 할당되었을 경우
                    # 지원자에게는 면접 시간을 할당하지 않고 다음 지원자로 넘어감
                    continue


# @admin.action(description="면접 시간 자동 배치")
# def set_interview_time(
#     self, request, queryset
# ):  # self = resume model , queryset = 체크했던 object들
#     times = [queryset.time for queryset in InterviewTime.objects.all()]
#     meta = self.model._meta

#     q = Resume.objects.annotate(c=Count("interview_time_choice")).order_by("c")

#     for i in q:
#         for j in i.interview_time_choice.all():
#             if j.time in times:
#                 time_num = 0
#                 s = Resume.objects.annotate()
#                 for (
#                     _resume
#                 ) in s:  # resume에 대해 call하는 부분 문제 어떤방식으로 call해야하나?
#                     if j.time == _resume.fixed_interview_time:
#                         time_num = time_num + 1
#                 if time_num == 1:
#                     plus20 = j.time + datetime.timedelta(minutes=20)
#                     a = Resume.objects.annotate()
#                     for Res in a:
#                         if plus20 == Res.fixed_interview_time:
#                             time_num = time_num + 1
#                     if time_num == 2:  # 2개 있을 때
#                         i.fixed_interview_time = plus20 + datetime.timedelta(minutes=20)
#                         i.save()
#                         j.is_fixed = True
#                         j.save()
#                         times.remove(j.time)
#                         break

#                     else:  # 1개 있을
#                         i.fixed_interview_time = plus20
#                         i.save()
#                         break

#                 else:  # 0개일때
#                     i.fixed_interview_time = j.time
#                     i.save()
#                     break


@admin.action(description="면접 장소 일괄 지정")
def set_interview_place(self, request, queryset):
    place = get_object_or_404(InterviewPlace)
    for query in queryset:
        query.interview_place = place
        query.save()


@admin.action(description="일괄 서류 불합격")
def set_doc_fail(self, request, queryset):
    for _resume in queryset:
        _resume.is_pass_document = False
        _resume.save()


@admin.action(description="일괄 서류 합격")
def set_doc_pass(self, request, queryset):
    for _resume in queryset:
        _resume.is_pass_document = True
        _resume.save()


@admin.action(description="일괄 최종 합격")
def set_final_pass(self, request, queryset):
    for _resume in queryset:
        _resume.is_pass_final = True
        _resume.save()


@admin.action(description="일괄 최종 불합격")
def set_final_fail(self, request, queryset):
    for _resume in queryset:
        _resume.is_pass_final = False
        _resume.save()


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "semester",
        "phone",
        "fixed_interview_time",
        "interview_place",
    )
    search_fields = ["name", "applicant__student_id", "introduce", "motivate"]
    actions = [
        get_all_resume,
        set_interview_time,
        set_interview_place,
        set_doc_fail,
        set_doc_pass,
        set_final_pass,
        set_final_fail,
    ]

    def get_ordering(self, request):
        return ["fixed_interview_time"]


admin.site.register(InterviewPlace)
admin.site.register(Recruitment)
admin.site.register(InterviewTime)

# Register your models here.
