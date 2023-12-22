FROM python:3.11.6-alpine3.18

WORKDIR /news

COPY . /news

RUN cd /news
RUN python -m venv venv
RUN source venv/bin/activate
RUN pip install --no-cache-dir --upgrade -r requirements.txt

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

EXPOSE 8000