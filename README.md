# Task Manager — FastAPI & Streamlit

A Dockerized Task Management application built with **FastAPI** as the backend REST API and **Streamlit** as the interactive frontend dashboard.

## Project Overview

Task Manager helps users create, organize, track, update, and complete tasks through a user-friendly dashboard.

The project uses Docker Compose to run the backend and frontend as separate services.

## Features

- Create, view, update, and delete tasks
- Set task priority and due dates
- Track task completion status
- Interactive Streamlit dashboard
- REST API powered by FastAPI
- API documentation with Swagger UI
- Docker and Docker Compose support

## Tech Stack

- Python
- FastAPI
- Streamlit
- Pydantic
- Requests
- Docker
- Docker Compose

## Project Structure

```text
Docker-FastAPI-Assignment/
│
├── main.py
├── streamlit_app.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .gitignore
└── README.md
```

## Run with Docker Compose

Make sure Docker Desktop is running.

Clone the repository:

```bash
git clone https://github.com/misbahs10/docker-fastapi-assignment.git
```

Open the project directory:

```bash
cd docker-fastapi-assignment
```

Build and start both services:

```bash
docker compose up --build -d
```

Check running containers:

```bash
docker compose ps
```

View logs:

```bash
docker compose logs
```

Stop services:

```bash
docker compose down
```

## Application URLs

| Service | URL |
|---|---|
| Streamlit Dashboard | http://localhost:8501 |
| FastAPI Backend | http://localhost:8000 |
| Swagger API Documentation | http://localhost:8000/docs |

## Docker Hub

Docker Hub Repository:

https://hub.docker.com/r/misbahsajjad/task-manager-api

## GitHub Repository

https://github.com/misbahs10/docker-fastapi-assignment

## Important Note

The current backend uses in-memory storage for tasks. Task data is not persisted when the backend process or container is recreated.

## Author

**Misbah Sajjad**

GitHub: https://github.com/misbahs10

LinkedIn: https://www.linkedin.com/in/misbahsajjad23