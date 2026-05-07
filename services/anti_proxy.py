from models.attendance import TempAttendance

def is_duplicate_student(session_id, student_id):
    existing = TempAttendance.query.filter_by(
        session_id=session_id,
        student_id=student_id
    ).first()
    return existing is not None
