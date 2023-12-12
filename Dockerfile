FROM ubuntu:latest

# konlpy 를 위한 환경 설정
ENV LANG=C.UTF-8
ENV TZ=Asia/Seoul
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update 
#RUN pip install --upgrade pip

# installing java jdk and java jre
RUN apt-get install -y default-jdk default-jre

# installing python3 and pip3
RUN apt install python3 -y

RUN apt-get install python3-pip -y
#RUN apt-get install python3-dev -y

# apt 정리 - 필요 없는 파일을 삭제해서 용량 줄이기
RUN rm -rf /var/lib/apt/lists/*

# 디렉토리 설정
WORKDIR /usr/src/app
COPY requirements.txt ./
COPY . .

# install konlpy dependencies: jpype, konlpy
RUN pip install jpype1-py3 konlpy

RUN pip install -r requirements.txt 



EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]