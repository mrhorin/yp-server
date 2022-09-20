FROM python:3

WORKDIR /usr/src/yp-server

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 7144

