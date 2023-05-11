# src/cache.py
import pickle
import os
import hashlib

import sys

# Determine the path to cache.py
cache_dir = os.path.join(os.path.dirname(os.path.abspath(sys.modules[__name__].__file__)), '..', 'cache')
os.makedirs(cache_dir, exist_ok=True)
cache_file = os.path.join(cache_dir, "cache.pkl")


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
