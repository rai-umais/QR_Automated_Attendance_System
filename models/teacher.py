import uuid
from datetime import datetime, UTC
from models.base import db

class Teacher(db.Model):
    __tablename__ = 'teachers'

    id         = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    name       = db.Column(db.String(100), nullable=False)
    email      = db.Column(db.String(150), nullable=False, unique=True)
    google_sub = db.Column(db.String(150), unique=True, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now(UTC))

    courses  = db.relationship('Course', backref='teacher', lazy=True)
    sessions = db.relationship('Session', backref='teacher', lazy=True)

    def __repr__(self):
        return f'<Teacher {self.email}>'