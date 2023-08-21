from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "search" ALTER COLUMN "telegram_channel" TYPE VARCHAR(2000) USING "telegram_channel"::VARCHAR(2000);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "search" ALTER COLUMN "telegram_channel" TYPE VARCHAR(100) USING "telegram_channel"::VARCHAR(100);"""
