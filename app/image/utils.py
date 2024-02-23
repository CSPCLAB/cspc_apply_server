import os
from django.utils.text import slugify


def image_rename(instance, filename):
    ext = filename.split(".")[-1]
    file_name = "{}.{}".format(slugify(instance.title), ext)
    return os.path.join("", file_name)
