from hashlib import sha256
from models import URLMap, db
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
    existing = URLMap.query.filter_by(code=slug).first()
    if existing:
        return existing.url
    return "no url"