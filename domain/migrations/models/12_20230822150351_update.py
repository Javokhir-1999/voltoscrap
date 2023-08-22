from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "post" ALTER COLUMN "pos_source_unique_id" TYPE VARCHAR(200) USING "pos_source_unique_id"::VARCHAR(200);
        ALTER TABLE "post" ALTER COLUMN "word" TYPE VARCHAR(200) USING "word"::VARCHAR(200);
        ALTER TABLE "search" ADD "facebook_channel" VARCHAR(2000);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "post" ALTER COLUMN "pos_source_unique_id" TYPE VARCHAR(20) USING "pos_source_unique_id"::VARCHAR(20);
        ALTER TABLE "post" ALTER COLUMN "word" TYPE VARCHAR(20) USING "word"::VARCHAR(20);
        ALTER TABLE "search" DROP COLUMN "facebook_channel";"""
