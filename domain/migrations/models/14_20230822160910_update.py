from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "comment" ALTER COLUMN "post_source_id" TYPE VARCHAR(200) USING "post_source_id"::VARCHAR(200);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "comment" ALTER COLUMN "post_source_id" TYPE VARCHAR(50) USING "post_source_id"::VARCHAR(50);"""
