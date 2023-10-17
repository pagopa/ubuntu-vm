FROM ubuntu:latest
COPY . .

CMD python ./script/status.py
