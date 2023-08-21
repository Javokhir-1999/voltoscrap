from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "comment" ALTER COLUMN "status" TYPE VARCHAR(8) USING "status"::VARCHAR(8);
        ALTER TABLE "post" ALTER COLUMN "status" TYPE VARCHAR(8) USING "status"::VARCHAR(8);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "post" ALTER COLUMN "status" TYPE VARCHAR(8) USING "status"::VARCHAR(8);
        ALTER TABLE "comment" ALTER COLUMN "status" TYPE VARCHAR(8) USING "status"::VARCHAR(8);"""
