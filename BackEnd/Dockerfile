FROM python:3.9.14-buster

# Install libglib2.0

RUN apt-get update && apt-get install libgl1 -y

# Install zip
RUN apt-get install unzip -y

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
COPY ./config.json /etc/config.json
CMD python manage.py runserver
