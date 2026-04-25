from flask import Blueprint, render_template, session
from routes.decorators import teacher_required

teacher_bp = Blueprint('teacher', __name__, url_prefix='/teacher')

@teacher_bp.route('/dashboard')
@teacher_required
def dashboard():
    return render_template('dashboard.html', name=session.get('user_name')) # now this is the joinja templating i think, we send the params
                                                    # to the html file, from the session of flask that we initialized in auth.py