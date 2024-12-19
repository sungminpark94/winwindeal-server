# 베이스 이미지 (본인 프로젝트에 맞는 버전 기입)
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# 종속성 파일 복사
COPY ./requirements.txt /wwd/

# 작업 디렉토리 설정
WORKDIR /wwd
RUN mkdir -p static staticfiles


# MySQL 클라이언트 설치
RUN apt-get update \
    && apt-get install -y default-libmysqlclient-dev build-essential pkg-config \
    && rm -rf /var/lib/apt/lists/*

# 종속성 설치
RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install gunicorn

# 애플리케이션 코드 복사
COPY ./app /wwd/app
WORKDIR /wwd/app



# 소켓 파일 생성 디렉토리 권한 설정
RUN mkdir -p /wwd && chmod -R 755 /wwd

# Gunicorn을 사용하여 애플리케이션 실행
# CMD ["gunicorn", "winwindeal_be.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]

# 변경된 코드: 스크립트를 사용하여 애플리케이션 실행
COPY ./scripts /scripts
RUN chmod +x /scripts/run.sh
CMD ["/scripts/run.sh"]