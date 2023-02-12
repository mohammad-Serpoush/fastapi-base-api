from datetime import timedelta
from redis.client import Redis


def get_data_from_cache(client: Redis, key: str = None) -> str:
    val = client.get(key)
    return val


def set_data_to_cache(
        client: Redis, key: str = None, value: str = None, expire: int = 3600
) -> bool:
    state = client.setex(key, timedelta(seconds=3600), value=value)  # todo time
    client.expire(key, expire)
    return state


def remove_data_from_cache(client: Redis, key: str = None):
    client.delete(key)
    return None


def get_password_data(client: Redis, *, code: str = None):
    data = get_data_from_cache(client, key="code")

    if data is None:
        state = set_data_to_cache(client, key="code", value=code)
        if state is True:
            data = get_data_from_cache(client, key="code")
    return data
