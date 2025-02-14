from django.db import models
from django.utils import timezone
from user.models import Applicant
from .utils import *


class TermType(models.TextChoices):
    SPRING = "spring"
    FALL = "fall"


class RecruitProcess(models.TextChoices):
    CLOSE = "close"
    APPLY = "apply"
    MIDDLE = "middle"
    FINAL = "final"


class Recruitment(models.Model):
    year = models.PositiveSmallIntegerField()
    term = models.CharField(max_length=10, choices=TermType.choices)
    start_time = models.DateField()
    document_deadline = models.DateField()
    announce_middle_time = models.DateTimeField()
    interview_start_time = models.DateField()
    interview_end_time = models.DateField()
    announce_final_time = models.DateTimeField()
    process = models.CharField(
        max_length=10, choices=RecruitProcess.choices, default=RecruitProcess.CLOSE
    )

    def check_process(self):
        now = timezone.now()

        if now >= self.announce_final_time:
            new_process = RecruitProcess.FINAL
        elif now >= self.announce_middle_time:
            new_process = RecruitProcess.MIDDLE
        elif now.date() >= self.start_time:
            new_process = RecruitProcess.APPLY
        else:
            new_process = RecruitProcess.CLOSE

        if self.process != new_process: 
            self.process = new_process
            self.save()

    def clean(self):
        if self.start_time >= self.document_deadline:
            raise ValidationError("지원 시작일은 서류 마감일보다 이전이어야 합니다.")
        if self.document_deadline >= self.announce_middle_time.date():
            raise ValidationError("서류 마감일은 중간 발표일보다 이전이어야 합니다.")
        if self.announce_middle_time.date() >= self.interview_start_time:
            raise ValidationError("중간 발표일은 면접 시작일보다 이전이어야 합니다.")
        if self.interview_start_time >= self.interview_end_time:
            raise ValidationError("면접 시작일은 면접 종료일보다 이전이어야 합니다.")
        if self.interview_end_time >= self.announce_final_time.date():
            raise ValidationError("면접 종료일은 최종 발표일보다 이전이어야 합니다.")

    def save(self, *args, **kwargs):
        self.full_clean()  # 저장 전에 유효성 검사 실행
        super().save(*args, **kwargs)

class InterviewTime(models.Model):
    time = models.DateTimeField(validators=[validate_interview_time])
    is_fixed = models.BooleanField(default=False)  # 면접 시간 모두 배정되었는지 여부

    def __str__(self):
        return self.time.strftime("%Y/%m/%d %H:%M:%S")


class InterviewPlace(models.Model):
    place = models.CharField(max_length=20)

    def __str__(self):
        return self.place


class Resume(models.Model):
    applicant = models.OneToOneField(Applicant, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    semester = models.PositiveSmallIntegerField()
    # 지원서 답변
    introduce = models.TextField(default="")
    motivate = models.TextField(default="")
    to_do = models.TextField(default="")
    etc = models.TextField(default="")

    interview_time_choice = models.ManyToManyField(
        InterviewTime, related_name="resumes"
    )
    fixed_interview_time = models.DateTimeField(null=True, blank=True)
    interview_requirement = models.TextField(default="")  # 면접 요구 사항
    interview_place = models.ForeignKey(
        InterviewPlace, on_delete=models.CASCADE, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_pass_document = models.BooleanField(default=True)
    is_pass_final = models.BooleanField(default=False)

    def __str__(self):
        return self.name


# Create your models here.
