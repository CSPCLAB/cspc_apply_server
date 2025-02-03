FROM python:3.8-slim-buster

WORKDIR /home/app/web

ENV HOME=/home/app
ENV APP_HOME=/home/app/web
ENV DEBUG_MODE=False
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV ENVIRONMENT=production
ENV DJANGO_SETTINGS_MODULE=cspc_web.settings.prod

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt .
RUN pip install --no-cache-dir --prefer-binary -r requirements.txt

COPY . .

RUN pip install python-dotenv

# 🔹 ENTRYPOINT에서 `.env` 또는 환경 변수를 로드하여 실행하도록 변경
CMD ["sh", "-c", "source /home/app/web/.env 2>/dev/null || true && exec gunicorn --bind 0.0.0.0:8000 cspc_web.wsgi:application"]
