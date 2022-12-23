FROM python:3.10-slim-buster

WORKDIR /src

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .


CMD [ "python", "main.py", "--interval", "501", "--tburl", "https://iotportal.atea.se/api/v1/integrations/http/dbdfa116-9e1c-18f5-f560-08c1b4711593"]

