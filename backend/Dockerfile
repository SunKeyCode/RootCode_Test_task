FROM python:3.11-slim-buster

COPY app /backend/app
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY start_app.sh backend/start_app.sh

WORKDIR /backend/app/

RUN ["chmod", "+x", "../start_app.sh"]

CMD ["../start_app.sh"]