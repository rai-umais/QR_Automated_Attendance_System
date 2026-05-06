from flask import Blueprint, jsonify,render_template

# blueprint is created so that if multiple routes are formed.
main_bp = Blueprint('main',__name__)

from flask import request

@main_bp.route('/')
def index():
    error = request.args.get('error')
    return render_template('index.html', error=error)

@main_bp.route('/health')
def health():
    return jsonify({'status':'Ok'})