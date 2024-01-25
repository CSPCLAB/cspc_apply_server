from django.db import models
from django.db.models.signals import post_init, post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser ,BaseUserManager
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, student_id, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not student_id:
            raise ValueError('The given student_id must be set')

        user = self.model(student_id=student_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, student_id, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(student_id, password, **extra_fields)

    def create_superuser(self, student_id, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(student_id, password, **extra_fields)

class Applicant(AbstractUser):
    student_id = models.CharField(max_length=20,unique=True)
    username = None
    USERNAME_FIELD = 'student_id'
    REQUIRED_FIELDS = []
    object = UserManager()
    def __str__(self):
        return self.student_id

class LabMaster(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField(max_length=30)
    phone = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    


# 랩짱 변경 시 기존 랩장 비활성화
@receiver(post_save, sender=LabMaster)
def create_master(sender, instance=None, created=False, **kwargs):
    if created:
        pre_masters = LabMaster.objects.exclude(id=instance.id)
        for master in pre_masters:
            master.is_active = False
            master.save()
