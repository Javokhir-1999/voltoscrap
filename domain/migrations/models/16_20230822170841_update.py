from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "comment" ADD "comment_source_unique_id" VARCHAR(200)  UNIQUE;
        CREATE UNIQUE INDEX "uid_comment_comment_12797f" ON "comment" ("comment_source_unique_id");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX "idx_comment_comment_12797f";
        ALTER TABLE "comment" DROP COLUMN "comment_source_unique_id";"""
