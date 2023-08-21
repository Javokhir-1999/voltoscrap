from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "post" ALTER COLUMN "url" DROP NOT NULL;
        ALTER TABLE "post" ALTER COLUMN "author" DROP NOT NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "post" ALTER COLUMN "url" SET NOT NULL;
        ALTER TABLE "post" ALTER COLUMN "author" SET NOT NULL;"""
