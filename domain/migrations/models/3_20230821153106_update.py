from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "comment" ADD "author_id" VARCHAR(50) NOT NULL;
        ALTER TABLE "comment" ADD "emoji" JSONB;
        ALTER TABLE "comment" ADD "source" VARCHAR(3);
        ALTER TABLE "comment" ADD "top_three_emoji" JSONB;
        ALTER TABLE "comment" ADD "post_source_id" VARCHAR(50);
        ALTER TABLE "post" ADD "author_id" VARCHAR(50);
        ALTER TABLE "post" ADD "source" VARCHAR(3);
        ALTER TABLE "post" ADD "emoji" JSONB;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "post" DROP COLUMN "author_id";
        ALTER TABLE "post" DROP COLUMN "source";
        ALTER TABLE "post" DROP COLUMN "emoji";
        ALTER TABLE "comment" DROP COLUMN "author_id";
        ALTER TABLE "comment" DROP COLUMN "emoji";
        ALTER TABLE "comment" DROP COLUMN "source";
        ALTER TABLE "comment" DROP COLUMN "top_three_emoji";
        ALTER TABLE "comment" DROP COLUMN "post_source_id";"""
