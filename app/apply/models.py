from django.db import models
from django.utils import timezone
from user.models import Applicant

class TermType(models.TextChoices):
    SPRING = 'spring'
    FALL = 'fall'

class RecruitProcess(models.TextChoices):
   CLOSE = 'close'
   APPLY = 'apply'
   MIDDLE = 'middle'
   FINAL = 'final'

class Recruitment(models.Model):
    year = models.PositiveSmallIntegerField()
    term = models.CharField(max_length=10, choices=TermType.choices)
    start_time = models.DateField()
    document_deadline = models.DateField()
    announce_middle_time = models.DateTimeField()
    interview_start_time = models.DateField()
    interview_end_time = models.DateField()
    announce_final_time = models.DateTimeField()
    process = models.CharField(max_length=10, choices=RecruitProcess.choices ,default=RecruitProcess.CLOSE)

    def check_process(self):
        now = timezone.now()
        if now >= self.announce_final_time :
            self.process = RecruitProcess.FINAL
        elif now >= self.announce_middle_time :
            self.process = RecruitProcess.MIDDLE
        elif now.date() >= self.start_time :
            self.process = RecruitProcess.APPLY
        else :
            self.process = RecruitProcess.CLOSE
        self.save()
    
class InterviewTime(models.Model):
    time = models.DateTimeField()
    is_fixed = models.BooleanField(default=False)

    def __str__(self):
        return self.time.strftime("%Y/%m/%d %H:%M:%S")
    
class InterviewPlace(models.Model):
    place = models.CharField(max_length=20)

    def __str__(self):
        return self.place

class Resume(models.Model):
    applicant = models.OneToOneField(Applicant,on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    semester = models.PositiveSmallIntegerField()
    #지원서 답변
    introduce = models.TextField(default='')
    motivate = models.TextField(default='')
    to_do = models.TextField(default='')
    etc = models.TextField(default='')

    interview_time_choice = models.ManyToManyField(InterviewTime,related_name="interview_time")
    fixed_interview_time = models.DateTimeField(null=True,blank=True)
    interview_requirement = models.TextField(default='')
    interview_place = models.ForeignKey(InterviewPlace,on_delete=models.CASCADE,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_pass_document = models.BooleanField(default=True)
    is_pass_final = models.BooleanField(default=False)
    

    def __str__(self):
        return self.name


# Create your models here.
