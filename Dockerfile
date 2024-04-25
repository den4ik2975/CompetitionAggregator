FROM ubuntu:latest
LABEL authors="den41"

ENTRYPOINT ["top", "-b"]