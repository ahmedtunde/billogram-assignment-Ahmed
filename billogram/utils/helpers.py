import uuid
from django.core.cache import cache




def generate_id():
    return uuid.uuid4().hex


def parse_query_params(request):
    if not request.query_params:
        return None
    query_str = ''
    query_str_list = list(request.query_params.items())
    for index, value in enumerate(request.query_params.items()):
        if (index + 1) == len(query_str_list):
            query_str += f"{value[0]}={value[1]}"
            break
        query_str += f"{value[0]}={value[1]}&"
    return query_str


def retrieve_from_redis(key):
    """
        This function retrieve from redis
        1. This function take one arguments {key}
        2. Retrieve the data of the key passed in
    """
    return cache.get(key)


def delete_from_redis(key):
    """ This function deteles a key and its data from redis"""
    return cache.delete(key)


def save_in_redis(key, data, timeout=None):
    """
        This function save in redis
        1. This function take three arguments key,
            data to be saved and timeout value
        2. Save the data with {key} arg as the key in redis
    """
    cache.set(key, data, timeout=timeout)

