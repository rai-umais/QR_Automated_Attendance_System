import uuid
from datetime import datetime,UTC
from models.base import db

class Student(db.Model):
    __tablename__ = 'Students'

    id = db.Column(db.String(50), primary_key = True, default=lambda: str(uuid.uuid4()))
    roll_number = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    google_sub = db.Column(db.String(150), unique=True, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now(UTC))


    def __repr__(self):
        return f'<Student {self.email}>'