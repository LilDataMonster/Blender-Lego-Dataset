FROM python:3.9-buster

ARG DEBIAN_FRONTEND noninteractive
ARG TZ America/New_York

USER root
ENV USER=root

RUN apt-get update -y && apt-get install -y ffmpeg libxi-dev libxxf86vm-dev libgl-dev &&\
    pip install blenderproc numpy ffmpeg-python pandas && echo "import blenderproc; blenderproc.init()" > test.py
RUN blenderproc run test.py && rm -rf /var/lib/apt/lists/* && rm test.py

CMD ["blenderproc", "run"]
