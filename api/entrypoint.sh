#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Trap errors and handle cleanup or logging if necessary
trap 'echo "Error occurred. Exiting script."; exit 1;' ERR

# Print the current working directory
echo "Current working directory is: $(pwd)"

# Function to check if the 'aerich' table exists
check_aerich_table_exists() {
  python3 <<EOF
from tortoise import Tortoise
import asyncio

async def check_table():
    try:
        from src.config import TORTOISE_ORM  # Direct import for better debugging
        print("TORTOISE_ORM loaded successfully:", TORTOISE_ORM)

        await Tortoise.init(config=TORTOISE_ORM)
        connection = Tortoise.get_connection('default')
        result = await connection.execute_query("SELECT 1 FROM information_schema.tables WHERE table_name = 'aerich'")
        await Tortoise.close_connections()
        exit(0 if result else 1)
    except Exception as e:
        import traceback
        print("Error Traceback:")
        traceback.print_exc()  # Print the full traceback for debugging
        exit(1)
    
asyncio.run(check_table())
EOF
}

# Check if aerich.ini exists
if [ ! -f "pyproject.toml" ]; then
  echo "pyproject.toml not found. Running aerich init..."
  aerich init -t src.config.TORTOISE_ORM
fi

# Run aerich init-db only if the aerich table does not exist
if ! check_aerich_table_exists; then
  echo "Aerich table not found. Running aerich init-db..."
  aerich init-db
fi

# Apply migrations
aerich upgrade

# Start the application
exec "$@"
