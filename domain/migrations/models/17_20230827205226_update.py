from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "search" RENAME COLUMN "post" TO "fb_post";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "search" RENAME COLUMN "fb_post" TO "post";"""
