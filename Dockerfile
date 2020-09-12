FROM python:3.8-alpine

WORKDIR /opt/app
COPY requirements.txt .
COPY main.py .
COPY templates/* ./templates/

RUN pip install -r requirements.txt
RUN chmod a+x main.py

EXPOSE 7878
CMD ./main.py