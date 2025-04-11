from hashlib import sha256
from models import URLMap, db
from functools import lru_cache
from flask import abort
import redis,os
# Connect to Redis server
cache = redis.Redis(host=os.getenv("REDIS_HOST", "redis"), port=6379, db=0, decode_responses=True)


def short_url(url):
    hashcode= sha256(url.encode()).hexdigest()[:8]
    existing = URLMap.query.filter_by(code=hashcode).first()
    if existing:
        return f"https://shorty/{hashcode}ihadit"
    new_data = URLMap(url=url, code=hashcode)
    db.session.add(new_data)
    db.session.commit()
    return f"https://shorty/{hashcode}"


def get_url(slug):
    url = cache.get(slug)
    if url:
        return url
    existing = URLMap.query.filter_by(code=slug).first()
    if existing:

        cache.set(slug, existing.url)
        return existing.url
    return abort(404)