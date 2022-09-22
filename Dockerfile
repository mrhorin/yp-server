FROM python:3

WORKDIR /yp-server
COPY . /yp-server

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 7144

