from django.db import models

# import model_helpers

# Create your models here.


class Apply_Image(models.Model):
    title = models.CharField(null=False, max_length=50)
    image = models.ImageField(null=False, upload_to="media/Apply")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "image"

    def __str__(self):
        return self.title


class Introduce_Image(models.Model):
    title = models.CharField(null=False, max_length=50)
    image = models.ImageField(null=False, upload_to="media/Introduce")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "image"

    def __str__(self):
        return self.title


class Login_Image(models.Model):
    title = models.CharField(null=False, max_length=50)
    image = models.ImageField(null=False, upload_to="media/Login")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "image"

    def __str__(self):
        return self.title


class Main_Image(models.Model):
    title = models.CharField(null=False, max_length=50)
    image = models.ImageField(null=False, upload_to="media/Main")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "image"

    def __str__(self):
        return self.title


class NotAllow_Image(models.Model):
    title = models.CharField(null=False, max_length=50)
    image = models.ImageField(null=False, upload_to="media/NotAllow")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "image"

    def __str__(self):
        return self.title


class Result_Image(models.Model):
    title = models.CharField(null=False, max_length=50)
    image = models.ImageField(null=False, upload_to="media/Result")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "image"

    def __str__(self):
        return self.title
