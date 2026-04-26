import uuid
from datetime import datetime, UTC
from models.base import db

class Session(db.Model):
    __tablename__ = 'sessions'

    id           = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    course_id    = db.Column(db.String(50), db.ForeignKey('courses.id'),  nullable=False)
    teacher_id   = db.Column(db.String(50), db.ForeignKey('teachers.id'), nullable=False)
    date         = db.Column(db.Date, nullable=False, default=datetime.now(UTC))
    started_at   = db.Column(db.DateTime, default=datetime.now(UTC))
    finalized_at = db.Column(db.DateTime, nullable=True)
    status       = db.Column(db.String(10), default='open')

    temp_records  = db.relationship('TempAttendance', backref='session', lazy=True)
    final_records = db.relationship('Attendance',     backref='session', lazy=True)

    def __repr__(self):
        return f'<Session {self.id} [{self.status}]>'