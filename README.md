# FastAPI Application with Celery, Redis, and PostgreSQL

This project is a FastAPI-based web application integrated with Celery for task management, Redis as a message broker, and PostgreSQL as the database. The services are orchestrated using Docker Compose.

## Getting Started

Use `run_app.sh` script to build and run the containers. Note that en OpenAI
API key will be needed inside a `worker/.env` to work.