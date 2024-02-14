from django.db import models

# import model_helpers

# Create your models here.


class Image(models.Model):
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to="_image/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
