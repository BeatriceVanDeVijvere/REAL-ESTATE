#!/bin/bash

# Build Docker images
docker build -f dags/scraper/Dockerfile -t airflow_scraper:latest ./dags/dags_pipe.py;

# Init Airflow 
docker compose up airflow-init;

# Run Airflow
docker-compose --env-file .env up -d;