from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "comment" ADD "reply_comment_id" UUID;
        ALTER TABLE "comment" ADD "reply_url" VARCHAR(500);
        ALTER TABLE "comment" ADD CONSTRAINT "fk_comment_comment_e6e55fdd" FOREIGN KEY ("reply_comment_id") REFERENCES "comment" ("id") ON DELETE SET NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "comment" DROP CONSTRAINT "fk_comment_comment_e6e55fdd";
        ALTER TABLE "comment" DROP COLUMN "reply_comment_id";
        ALTER TABLE "comment" DROP COLUMN "reply_url";"""
