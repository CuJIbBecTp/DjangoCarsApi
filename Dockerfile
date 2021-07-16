FROM python:3.8.0

RUN pip install --upgrade pip
ADD . /DjangoCarsApi
WORKDIR /DjangoCarsApi
RUN pip install -r requirements.txt
EXPOSE 8000