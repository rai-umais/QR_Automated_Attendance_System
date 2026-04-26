import uuid
from datetime import datetime, UTC
from models.base import db

class TempAttendance(db.Model):
    __tablename__ = 'temp_attendance'

    id                 = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id         = db.Column(db.String(50), db.ForeignKey('sessions.id'), nullable=False)
    student_id         = db.Column(db.String(50), db.ForeignKey('students.id'), nullable=False)
    scanned_at         = db.Column(db.DateTime, default=datetime.now(UTC))
    device_fingerprint = db.Column(db.String(300), nullable=True)

    student = db.relationship('Student', backref='temp_records')

    def __repr__(self):
        return f'<TempAttendance session={self.session_id} student={self.student_id}>'


class Attendance(db.Model):
    __tablename__ = 'attendance'

    id           = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id   = db.Column(db.String(50), db.ForeignKey('sessions.id'), nullable=False)
    student_id   = db.Column(db.String(50), db.ForeignKey('students.id'), nullable=False)
    date         = db.Column(db.Date, nullable=False)
    status       = db.Column(db.String(1), default='A')
    finalized_at = db.Column(db.DateTime, default=datetime.now(UTC))

    student = db.relationship('Student', backref='attendance_records')

    def __repr__(self):
        return f'<Attendance {self.student_id} {self.date} {self.status}>'