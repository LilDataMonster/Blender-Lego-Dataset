FROM python:3.9-slim

WORKDIR /root
RUN apt-get update -y && apt-get install -y ffmpeg libcurl4
RUN pip install fiftyone ipython torch torchvision tensorflow tensorflow-datasets

COPY fo_setup.py /root

CMD python fo_setup.py
