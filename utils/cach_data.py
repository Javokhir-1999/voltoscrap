from config.redis_settings import REDIS_CONN
def cach_data(instance,key=None):
    try:
        if not key:
            key=instance.id
        REDIS_CONN.set(key,instance.json())
    except Exception as e:
        print("redis exception:", e)

def get_cached(key, dto_model):
    try:
        data = REDIS_CONN.get(key)
        if data:
            return dto_model.parse_raw(data)
        return None
    except Exception as e:
        print("redis exception:", e)
        return None

def clear_cach(key):
    try:
        REDIS_CONN.delete(key)
    except Exception as e:
        print("redis exception:", e)