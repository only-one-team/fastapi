FROM ubuntu:latest
RUN apt-get update && apt-get install -y --no-install-recommends && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip

# installing java jdk and java jre
RUN apt-get install -y default-jdk default-jre

# installing python3 and pip3
RUN apt-get install -y python3-pip python3-dev


WORKDIR /usr/src/app
COPY requirements.txt ./
COPY . .

RUN pip install -r requirements.txt 


EXPOSE 8000
CMD ["python", "-m", "uvicorn", "app:app", "--port", "8000", "--reload"]