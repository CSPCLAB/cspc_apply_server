import os
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from rest_framework.authentication import BasicAuthentication
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# API 문서화 설정
schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    url=os.getenv("HOST"),  # 환경 변수에서 가져오기
    public=True,
    permission_classes=[permissions.AllowAny],
    authentication_classes=[BasicAuthentication],
)

# URL 패턴 정의
urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path("admin/", admin.site.urls),
    path("api/apply/", include("apply.urls")),
    path("api/user/", include("user.urls")),

    # Swagger & Redoc API 문서화
    path("api/swagger.json", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("api/swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("api/redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
