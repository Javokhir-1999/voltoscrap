from tortoise import Tortoise

from config.settings import ORM_CREDENTIALS


async def init_db(stage: str = "dev"):
    await Tortoise.init(config=ORM_CREDENTIALS)
    print("Tortoise initialized.......✅")
