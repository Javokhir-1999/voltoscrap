ORM_CREDENTIALS = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "database": "scrap_db",
                "host": "127.0.0.1",
                "password": "NsYi7#se4Q)0",
                "port": 5432,
                "user": "sc_user",
            },
        }
    },
    "apps": {
        "models": {
            "models": ["domain.models", "aerich.models"],
            "default_connection": "default",
        }
    },
}


SERVICES = {
    "sc_service":{"ip":"127.0.0.1", "port":7200},
}