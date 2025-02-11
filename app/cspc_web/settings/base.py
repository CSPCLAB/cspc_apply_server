# cspc_web/settings/base.py
import os
from pathlib import Path
from dotenv import load_dotenv
from django.core.management.utils import get_random_secret_key

BASE_DIR = Path(__file__).resolve().parent.parent.parent  # settings 폴더 기준으로 2단계 상위

load_dotenv()

# 공통 SECRET_KEY 처리
if not os.environ.get("SECRET_KEY"):
    # .env에 없다면 임의 생성
    random_key = get_random_secret_key()
    with open(os.path.join(BASE_DIR, ".env"), "a") as f:
        f.write(f"\nSECRET_KEY={random_key}")
    SECRET_KEY = random_key
else:
    SECRET_KEY = os.environ["SECRET_KEY"]

# DEBUG는 일단 False 기본
DEBUG = False

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# 기본 앱들
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "whitenoise.runserver_nostatic",

    # 3rd party
    "storages",
    "corsheaders",
    "drf_yasg",
    "rest_framework",

    # local apps
    "apply",
    "user",
    "image",
]

MIDDLEWARE = [
    "whitenoise.middleware.WhiteNoiseMiddleware",  
    "cspc_web.middleware.HealthCheckMiddleware",
    "django.middleware.common.CommonMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "cspc_web.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "cspc_web.wsgi.application"

# Database (SQLite 기본)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

# Password validators
AUTH_USER_MODEL = "user.Applicant"
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "ko"
TIME_ZONE = "Asia/Seoul"
USE_I18N = True
USE_TZ = False

STATIC_URL = "/api/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/api/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CORS_ORIGIN_ALLOW_ALL = True

# DRF & Swagger 기본 설정
REST_FRAMEWORK = {
    "DATETIME_FORMAT": "%Y-%m-%d %H:%M:%S",
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.BasicAuthentication",
    ],
}
SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Basic": {
            "type": "basic",
        },
    },
}

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8000",
    "http://localhost:3000",
]
