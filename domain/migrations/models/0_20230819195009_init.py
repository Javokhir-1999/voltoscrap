from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "search" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "created_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "modified_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "description" VARCHAR(255),
    "word" TEXT,
    "status" VARCHAR(7) NOT NULL
);
COMMENT ON COLUMN "search"."status" IS 'NEW: new\nPARSING: parsing\nPARSED: parsed';
CREATE TABLE IF NOT EXISTS "post" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "created_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "modified_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "description" VARCHAR(255),
    "text" TEXT,
    "url" VARCHAR(1000) NOT NULL,
    "media" JSONB,
    "date" TIMESTAMPTZ,
    "top_three_emoji" JSONB,
    "shares" INT   DEFAULT 0,
    "comments_count" INT   DEFAULT 0,
    "status" VARCHAR(10) NOT NULL,
    "data" JSONB,
    "search_id" UUID REFERENCES "search" ("id") ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS "idx_post_search__9a7a11" ON "post" ("search_id");
COMMENT ON COLUMN "post"."status" IS 'UNANALIZED: unanalized\nANALIZED: analized\nFAILED: failed';
CREATE TABLE IF NOT EXISTS "comment" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "created_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "modified_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "description" VARCHAR(255),
    "text" TEXT,
    "url" VARCHAR(1000) NOT NULL,
    "media" JSONB,
    "date" TIMESTAMPTZ,
    "status" VARCHAR(10) NOT NULL,
    "data" JSONB,
    "post_id" UUID REFERENCES "post" ("id") ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS "idx_comment_post_id_298e22" ON "comment" ("post_id");
COMMENT ON COLUMN "comment"."status" IS 'UNANALIZED: unanalized\nANALIZED: analized\nFAILED: failed';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
