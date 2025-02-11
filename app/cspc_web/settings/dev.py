# cspc_web/settings/dev.py
from .base import *

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# 개발용 DB 세팅 (ex: SQLite)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# 로컬 static/media (base.py의 설정 그대로 쓰면 됨)
STATIC_URL = "/static/"
MEDIA_URL = "/media/"

# 혹은 CSRF_TRUSTED_ORIGINS 개발용 추가
CSRF_TRUSTED_ORIGINS += [
    "http://127.0.0.1:3000",
]
