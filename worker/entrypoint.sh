#!/bin/sh

# Debug: Print current working directory and list files
echo "Current working directory: $(pwd)"
echo "Files in working directory:"
ls -R

# Debug: Print Python path
echo "PYTHONPATH: $PYTHONPATH"

# Debug: Test importing the Celery app
echo "Testing Celery app import..."
python -c "from src.worker import celery_worker; print('Celery app imported successfully')"

# Start the Celery worker
echo "Starting Celery worker..."
exec celery -A src.worker.celery_worker worker --loglevel=info
