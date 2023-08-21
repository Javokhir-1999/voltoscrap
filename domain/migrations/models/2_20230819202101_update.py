from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "comment" ADD "author" VARCHAR(50) NOT NULL;
        ALTER TABLE "post" ADD "tone" VARCHAR(100);
        ALTER TABLE "post" ADD "summary" VARCHAR(500);
        ALTER TABLE "post" ADD "author" VARCHAR(50) NOT NULL;
        ALTER TABLE "post" DROP COLUMN "shares1";
        ALTER TABLE "search" ADD "telegram_limit" INT   DEFAULT 5;
        ALTER TABLE "search" ADD "telegram_channel" VARCHAR(100);
        ALTER TABLE "search" ADD "use_telegram" BOOL   DEFAULT False;
        ALTER TABLE "search" ADD "facebook_limit" INT   DEFAULT 10;
        ALTER TABLE "search" ADD "use_facebook" BOOL   DEFAULT False;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "post" ADD "shares1" INT   DEFAULT 0;
        ALTER TABLE "post" DROP COLUMN "tone";
        ALTER TABLE "post" DROP COLUMN "summary";
        ALTER TABLE "post" DROP COLUMN "author";
        ALTER TABLE "search" DROP COLUMN "telegram_limit";
        ALTER TABLE "search" DROP COLUMN "telegram_channel";
        ALTER TABLE "search" DROP COLUMN "use_telegram";
        ALTER TABLE "search" DROP COLUMN "facebook_limit";
        ALTER TABLE "search" DROP COLUMN "use_facebook";
        ALTER TABLE "comment" DROP COLUMN "author";"""
