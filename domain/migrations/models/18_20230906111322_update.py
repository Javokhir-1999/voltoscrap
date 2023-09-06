from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "comment" ADD "search_id" UUID;
        ALTER TABLE "comment" ADD CONSTRAINT "fk_comment_search_4628b3bb" FOREIGN KEY ("search_id") REFERENCES "search" ("id") ON DELETE SET NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "comment" DROP CONSTRAINT "fk_comment_search_4628b3bb";
        ALTER TABLE "comment" DROP COLUMN "search_id";"""
