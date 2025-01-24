# 베이스 이미지
FROM python:3.8-slim

# 작업 디렉토리 생성
RUN mkdir -p /home/app

# 환경 변수 설정
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
ENV DEBUG_MODE=False
ENV PYTHONDONTWRITEBYTECODE=1 
ENV PYTHONUNBUFFERED=1        
ENV ENVIRONMENT=production   

RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# 시스템 패키지 업데이트 및 필수 패키지 설치
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*  # 캐시 제거로 이미지 크기 최소화

# Python 패키지 설치
COPY ./requirements.txt $APP_HOME/requirements.txt
RUN pip install --no-cache-dir --upgrade -r $APP_HOME/requirements.txt

# 애플리케이션 코드 복사
COPY . $APP_HOME

# 정적 파일 수집 (배포용)
RUN python manage.py collectstatic --noinput --clear

# 권한 설정 및 사용자 계정 생성
RUN addgroup --system appgroup && adduser --system --group appuser
RUN chown -R appuser:appgroup $APP_HOME
USER appuser

# 기본 실행 명령 (Django Gunicorn 서버 실행)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "cspc_web.wsgi:application"]
