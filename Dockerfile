FROM python:3.9.1
ADD . /python-fast-api
WORKDIR /python-fast-api
RUN pip install -r requirements.txt