# Use a lightweight Python image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

ENV PYTHONPATH=/app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code into the container
COPY ./src ./src
COPY ./entrypoint.sh ./entrypoint.sh


# Expose the application port
EXPOSE 8000

# Set the entrypoint
ENTRYPOINT ["./entrypoint.sh"]

# Run the FastAPI app with Uvicorn in reload mode
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]