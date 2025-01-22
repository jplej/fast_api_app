from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "enriched_stocks" (
    "symbol" VARCHAR(10) NOT NULL  PRIMARY KEY,
    "name" VARCHAR(255),
    "currency" VARCHAR(10),
    "founding_year" INT,
    "country" VARCHAR(100),
    "founder" VARCHAR(255),
    "current_ceo" VARCHAR(255),
    "market_cap" VARCHAR(50),
    "url_website" VARCHAR(255),
    "description" TEXT,
    "industry" VARCHAR(100),
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "enriched_stocks";"""
