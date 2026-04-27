from flask import Blueprint, render_template, request, jsonify, session
from datetime import datetime, UTC
from models.base import db
from models.student import Student
from models.attendance import TempAttendance
from services.qr_generator import verify_qr_token
from services.anti_proxy import is_duplicate_student, is_duplicate_device
from routes.decorators import student_required

student_bp = Blueprint('student', __name__, url_prefix='/student')

@student_bp.route('/scan')
def scan_page():
    token = request.args.get('token')
    if not token:
        return render_template('scan.html',
                               error='Invalid QR. Please scan again.')
    payload = verify_qr_token(token)
    if not payload:
        return render_template('scan.html',
                               error='QR expired. Please scan the latest one.')
    logged_in = 'user_id' in session and session.get('user_role') == 'Student'
    return render_template('scan.html',
                           token=token,
                           logged_in=logged_in,
                           name=session.get('user_name'))

@student_bp.route('/submit', methods=['POST'])
@student_required
def submit_attendance():
    data = request.json
    token = data.get('token')
    device_fingerprint = data.get('fingerprint')

    payload = verify_qr_token(token)
    if not payload:
        return jsonify({'error': 'QR expired. Please scan the latest QR.'}), 400

    session_id = payload['session_id']

    from models.session import Session
    active_session = Session.query.get(session_id)
    if not active_session or active_session.status != 'open':
        return jsonify({'error': 'Session is no longer active.'}), 400

    student_id = session['user_id']

    if is_duplicate_student(session_id, student_id):
        return jsonify({'error': 'You already marked your attendance.'}), 400

    if is_duplicate_device(session_id, device_fingerprint):
        return jsonify({'error': 'This device was already used.'}), 400

    record = TempAttendance(
        session_id=session_id,
        student_id=student_id,
        scanned_at=datetime.now(UTC),
        device_fingerprint=device_fingerprint
    )
    db.session.add(record)
    db.session.commit()

    return jsonify({
        'message': f'Attendance marked! Welcome {session["user_name"]}'
    }), 200