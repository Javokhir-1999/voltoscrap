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



"""


create database scrap_db;
create user sc_user with encrypted password 'NsYi7#se4Q)0';
grant all privileges on database scrap_db to sc_user;

"""