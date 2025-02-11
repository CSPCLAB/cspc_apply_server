# cspc_web/settings/prod.py
from .base import *

DEBUG = False

# ALLOWED_HOSTS = [
#     "apply.cspc.me", 
#     "dn9maygc9bxl1.cloudfront.net", # CloudFront
#     "ApplyS-Backe-PwdxXG8Mo9l7-1514720448.ap-northeast-2.elb.amazonaws.com", # ALB
#     "0.0.0.0", 
#     "127.0.0.1"
# ]

ALLOWED_HOSTS = ["*"]

# 예: PostgreSQL
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB", "dbname"),
        "USER": os.environ.get("POSTGRES_USER", "user"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "password"),
        "HOST": os.environ.get("POSTGRES_HOST", "db"),
        "PORT": os.environ.get("POSTGRES_PORT", 5432),
    }
}


# AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
# AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
# AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
# AWS_S3_REGION_NAME = os.environ.get("AWS_S3_REGION_NAME", "ap-northeast-2")
# AWS_DEFAULT_ACL = None
# AWS_S3_OBJECT_PARAMETERS = {
#     "CacheControl": "max-age=86400",
# }
# AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"

# # static / media
# STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
# DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

# STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/static/"
# MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/media/"

# CSRF
CSRF_TRUSTED_ORIGINS += [
    "https://apply.cspc.me",
]
