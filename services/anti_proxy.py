from models.attendance import TempAttendance

def is_duplicate_student(session_id, student_id):
    existing = TempAttendance.query.filter_by(
        session_id=session_id,
        student_id=student_id
    ).first()
    return existing is not None

def is_duplicate_device(session_id, device_fingerprint):
    if not device_fingerprint:
        return False
    existing = TempAttendance.query.filter_by(
        session_id=session_id,
        device_fingerprint=device_fingerprint
    ).first()
    return existing is not None