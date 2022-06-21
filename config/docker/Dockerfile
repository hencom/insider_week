FROM python:3.10
ENV PYTHONUNBUFFERED 1
RUN mkdir /config
RUN ls -l
RUN pwd
ADD ./requirements.pip /config
RUN pip install -r /config/requirements.pip