# Dockerized FastAPI Task Manager

A Task Management application built with **FastAPI**, **Streamlit**, and **Docker**. It provides a REST API for managing tasks and an interactive dashboard for creating, updating, completing, and deleting tasks.

## Features

- Create, read, update, and delete tasks (CRUD).
- Interactive Streamlit dashboard.
- Task priorities: Low, Medium, High.
- Due dates and task duration.
- Task difficulty levels.
- Mark tasks as completed.
- FastAPI Swagger API documentation.
- Docker containerization.
- Docker Compose for running backend and frontend together.

## Technologies Used

- Python 3.12
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

### 1. Clone the repository

```bash
git clone https://github.com/misbahs10/docker-fastapi-assignment.git
```

### 2. Navigate to the project directory

```bash
cd docker-fastapi-assignment
```

### 3. Build and start containers

```bash
docker compose up --build -d
```

### 4. Access the application

| Service | URL |
|---|---|
| Streamlit Dashboard | http://localhost:8501 |
| FastAPI Backend | http://localhost:8000 |
| Swagger API Docs | http://localhost:8000/docs |

### 5. Check running containers

```bash
docker compose ps
```

### 6. Stop containers

```bash
docker compose down
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API home |
| GET | `/tasks` | Get all tasks |
| GET | `/tasks/{task_id}` | Get a specific task |
| POST | `/tasks` | Create a task |
| PUT | `/tasks/{task_id}` | Update a task |
| DELETE | `/tasks/{task_id}` | Delete a task |

## Docker Hub

Docker image:

```bash
docker pull misbahsajjad/task-manager-api:2.0
```

[View Docker Hub Repository](https://hub.docker.com/r/misbahsajjad/task-manager-api)

## Important Note

This project currently uses in-memory storage for tasks. Task data is not persistent and may be lost when the backend process or container restarts.

## Author

**Misbah Sajjad**

- GitHub: https://github.com/misbahs10
- LinkedIn: https://www.linkedin.com/in/misbahsajjad23/
