#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Check if aerich.ini exists
if [ ! -f "/app/aerich.ini" ]; then
  echo "aerich.ini not found. Running aerich init..."
  aerich init -t app.config.TORTOISE_ORM
fi

# Apply migrations
aerich upgrade

# Start the application
exec "$@"
