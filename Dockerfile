# 베이스 이미지 (본인 프로젝트에 맞는 버전 기입)
FROM python:3.12-slim
WORKDIR /usr/src
RUN apt-get -y update
RUN apt-get install -y wget curl unzip  # curl 추가

RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt -y install ./google-chrome-stable_current_amd64.deb

# ChromeDriver 설치 (특정 버전을 직접 지정)
RUN wget -O /tmp/chromedriver.zip https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/120.0.6099.109/linux64/chromedriver-linux64.zip
RUN mkdir chrome
RUN unzip /tmp/chromedriver.zip -d /usr/src/chrome

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# 종속성 파일 복사
COPY ./requirements.txt /wwd/

# 작업 디렉토리 설정
WORKDIR /wwd
RUN mkdir -p staticfiles

#셀레니움 활용하기 위함
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libnss3 \
    libgconf-2-4 \
    libfontconfig1 \
    wget \
    && rm -rf /var/lib/apt/lists/*

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