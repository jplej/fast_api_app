from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "users" (
    "user_id" SERIAL NOT NULL PRIMARY KEY,
    "email" VARCHAR(255) NOT NULL UNIQUE,
    "username" VARCHAR(150) NOT NULL UNIQUE,
    "first_name" VARCHAR(50) NOT NULL,
    "last_name" VARCHAR(50) NOT NULL,
    "hashed_password" VARCHAR(128) NOT NULL,
    "is_active" BOOL NOT NULL  DEFAULT True,
    "role" VARCHAR(50) NOT NULL,
    "phone_number" VARCHAR(20)
);
CREATE TABLE IF NOT EXISTS "questrade_api_keys" (
    "key_id" SERIAL NOT NULL PRIMARY KEY,
    "key_type" VARCHAR(255) NOT NULL,
    "api_key" VARCHAR(255) NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "user_id_id" INT NOT NULL REFERENCES "users" ("user_id") ON DELETE CASCADE,
    CONSTRAINT "uid_questrade_a_user_id_b6cafe" UNIQUE ("user_id_id", "key_type")
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
