from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "post" ADD "pos_source_unique_id" VARCHAR(20)  UNIQUE;
        CREATE UNIQUE INDEX "uid_post_pos_sou_33caae" ON "post" ("pos_source_unique_id");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX "idx_post_pos_sou_33caae";
        ALTER TABLE "post" DROP COLUMN "pos_source_unique_id";"""
