from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "comment" ADD "tone" VARCHAR(100);
        ALTER TABLE "comment" ADD "summary" VARCHAR(500);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "comment" DROP COLUMN "tone";
        ALTER TABLE "comment" DROP COLUMN "summary";"""
