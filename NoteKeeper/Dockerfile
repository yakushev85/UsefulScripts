FROM python:3.12.10

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install fastapi uvicorn pyjwt bcrypt sqlmodel mysqlclient

EXPOSE 8080
WORKDIR /app
COPY ./main.py .

