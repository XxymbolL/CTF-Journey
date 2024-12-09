from functools import wraps
import os
import jwt
from flask import redirect, request, url_for
import psycopg2

def authenticated(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.cookies.get('token')
        if not token:
            return redirect(url_for('login'))

        try:
            decoded = jwt.decode(token, os.environ.get('SECRET_KEY'), algorithms=['HS256'])
        except jwt.exceptions.InvalidTokenError:
            return redirect(url_for('login'))

        db = psycopg2.connect(os.environ.get('DATABASE_URL'))
        with db.cursor() as cursor:
            cursor.execute('SELECT * FROM students WHERE username = %s', (decoded['sub'],))
            user = cursor.fetchone()
            if not user:
                return redirect(url_for('login'))
        return f(*args, **kwargs)
    return wrapper
