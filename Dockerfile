FROM ubuntu:latest
COPY . .

RUN apt-get update -y
RUN apt-get install -y git pip python3 nodejs

RUN pip install -r requirements.txt



CMD python3 ./status.py
