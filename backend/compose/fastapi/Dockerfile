FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app


ADD requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000

COPY . /app/