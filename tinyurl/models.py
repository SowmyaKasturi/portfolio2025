from flask_sqlalchemy import SQLAlchemy
from pendulum import now
db = SQLAlchemy()

class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(512), nullable=False)
    code = db.Column(db.String(64), nullable=False)
    created_at = db.Column(db.DateTime, default=now())
