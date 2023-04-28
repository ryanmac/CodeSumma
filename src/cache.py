# src/cache.py
import pickle
import os
import hashlib

cache_file = "cache.pkl"


def hash_key(prompt_object):
    return hashlib.sha256(str(prompt_object).encode()).hexdigest()


def load_cache():
    if not os.path.exists(cache_file):
        return {}

    with open(cache_file, "rb") as f:
        cache = pickle.load(f)
    return cache


def save_cache(cache):
    with open(cache_file, "wb") as f:
        pickle.dump(cache, f)


def get_cache(prompt_object, cache):
    key = hash_key(prompt_object)
    return cache.get(key)


def set_cache(prompt_object, response, cache):
    key = hash_key(prompt_object)
    cache[key] = response
    save_cache(cache)
