FROM ubuntu:latest
COPY . .

RUN apt-get update -y
RUN apt-get install -y git pip python3 nodejs vim curl iputils-ping wget default-jre-headless

RUN pip install -r requirements.txt


EXPOSE 8080

ENTRYPOINT ["python3",  "./status.py"]
