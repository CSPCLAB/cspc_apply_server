from django.db import models
from .utils import *

# import model_helpers

# Create your models here.


class Image(models.Model):
    title = models.CharField(null=False, max_length=50)
    image = models.ImageField(
        null=False,
        upload_to=image_rename,
        validators=[validate_file_size],
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "image"

    def __str__(self):
        return self.title
