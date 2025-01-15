import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgres://postgres:password@db:5432/postgres")

TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {
            "models": ["app.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}
