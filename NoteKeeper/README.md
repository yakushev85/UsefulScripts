# Notekeeper REST API

This project was created using FastAPI, MySQL and Docker.

## Step 1

Build application: `docker compose build`.

## Step 2

Run docker using `docker compose up`. If backend container doesn't start and shows `Can't connect to server on 'notekeeper_database' (115)`, use `docker container start notekeeper_backend`.

## Test

API documentation: http://localhost:8080/docs 

