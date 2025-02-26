
FROM python:3.8-slim-buster

WORKDIR /app

RUN pip3 install flask[async] flask-jwt-extended  flask-bcrypt flask-cors tinydb opencv-python-headless numpy scipy gunicorn

COPY . .
RUN chmod -R 777 /app 

ENTRYPOINT ["sh","./gunicorn.sh"]