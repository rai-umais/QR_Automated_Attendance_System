from flask import Blueprint, render_template, session
from routes.decorators import student_required

student_bp = Blueprint('student', __name__, url_prefix='/student')

@student_bp.route('/scan')
@student_required
def scan_page():
    return render_template('scan.html', name=session.get('user_name'))