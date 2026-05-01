import jwt
import qrcode
import base64
import os
from io import BytesIO
from datetime import datetime, timezone, timedelta
from flask import current_app

def get_base_url():
    # on Railway this env var will be set to your Railway URL
    # locally it falls back to localhost
    return os.environ.get('APP_BASE_URL', 'http://localhost:5000')

def generate_qr_token(session_id):
    payload = {
        'session_id': session_id,
        'exp': datetime.now(timezone.utc) + timedelta(seconds=30), # ← 30 seconds
        'iat': datetime.now(timezone.utc)
    }
    token = jwt.encode(
        payload,
        current_app.config['SECRET_KEY'],
        algorithm='HS256'
    )
    return token

def verify_qr_token(token):
    try:
        payload = jwt.decode(
            token,
            current_app.config['SECRET_KEY'],
            algorithms=['HS256']
        )
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def generate_qr_image(token):
    base_url = get_base_url()
    scan_url = f"{base_url}/student/scan?token={token}"
    print(f"QR encodes: {scan_url}")

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4
    )
    qr.add_data(scan_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    return base64.b64encode(buffer.getvalue()).decode('utf-8')