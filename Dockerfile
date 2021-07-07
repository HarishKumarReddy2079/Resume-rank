FROM python:3.6.9
ADD . /python-flask
WORKDIR /python-flask
RUN pip install -r requirements.txt
RUN pip install Flask gunicorn
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app