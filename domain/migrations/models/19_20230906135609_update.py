from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "search" ADD "fb_posts_count" INT   DEFAULT 0;
        ALTER TABLE "search" ADD "fb_comments_count" INT   DEFAULT 0;
        ALTER TABLE "search" ADD "tg_posts_count" INT   DEFAULT 0;
        ALTER TABLE "search" ADD "tg_comments_count" INT   DEFAULT 0;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "search" DROP COLUMN "fb_posts_count";
        ALTER TABLE "search" DROP COLUMN "fb_comments_count";
        ALTER TABLE "search" DROP COLUMN "tg_posts_count";
        ALTER TABLE "search" DROP COLUMN "tg_comments_count";"""
