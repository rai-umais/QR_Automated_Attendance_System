from datetime import datetime, UTC
from models.base import db
from models.session import Session

def start_session(course_id, teacher_id, mode='normal', custom_seconds=None, master_xlsx_path=None):
    existing = Session.query.filter_by(
        course_id=course_id,
        status='open'
    ).first()
    if existing:
        return existing

    new_session = Session(
        course_id  = course_id,
        teacher_id = teacher_id,
        date       = datetime.now(UTC).date(),
        started_at = datetime.now(UTC),
        status     = 'open',
        mode       = mode,
        custom_seconds = custom_seconds,
        master_xlsx_path = master_xlsx_path
    )
    db.session.add(new_session)
    db.session.commit()
    return new_session

def get_active_session(course_id):
    return Session.query.filter_by(
        course_id=course_id,
        status='open'
    ).first()

def get_teacher_active_session(teacher_id):
    """Return any open session for this teacher, regardless of course."""
    return Session.query.filter_by(
        teacher_id=teacher_id,
        status='open'
    ).first()

def close_session(session_id):
    s = db.session.get(Session, session_id)
    if s:
        s.status       = 'closed'
        s.finalized_at = datetime.now(UTC)
        db.session.commit()
    return s