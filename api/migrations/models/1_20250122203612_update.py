from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "questrade_api_keys";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
