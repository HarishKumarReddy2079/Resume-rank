FROM python:3.6.9
ADD . /python-flask
WORKDIR /python-flask
RUN pip install -r requirements.txt