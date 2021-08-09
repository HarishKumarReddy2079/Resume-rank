FROM python:3.6.9
ADD . /python-flask
WORKDIR /python-flask
RUN pip3 install -r requirements.txt
RUN pip3 install Flask gunicorn
COPY . .
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]