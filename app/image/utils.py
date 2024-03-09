import os
from django.utils.text import slugify
from django.core.exceptions import ValidationError


def validate_file_size(value):
    max_file_size = 20 * 1024 * 1024  # 20MB
    if value.size > max_file_size:
        raise ValidationError(
            f"파일 크기는 {max_file_size // (1024 * 1024)}MB를 초과할 수 없습니다."
        )


def image_rename(instance, filename):
    ext = filename.split(".")[-1]
    file_name = "{}.{}".format(slugify(instance.title), ext)
    return os.path.join("", file_name)
