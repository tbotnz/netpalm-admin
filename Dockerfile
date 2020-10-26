FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine 

COPY requirements.txt /app
RUN pip3 install -r requirements.txt 

COPY . /app
