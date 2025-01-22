FROM python:3.10-slim

# Set PYTHONPATH
ENV PYTHONPATH=/app

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ./src ./src 
COPY ./entrypoint.sh ./entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]