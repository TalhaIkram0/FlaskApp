from flask import Blueprint, request, session
from werkzeug.security import check_password_hash, generate_password_hash

from app.db import get_db


bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=('POST',))
def login():
    username = request.form['username']
    password = request.form['password']
    db = get_db()
    error = None
    user = db.execute('SELECT * FROM user WHERE username = ?', (username,)).fetchone()

    if user is None:
        error = 'Incorrect username.'
    elif not check_password_hash(user['password'], password):
        error = 'Incorrect password.'

    if error is None:
        session.clear()
        session['username'] = user['username']
        return "User was logged in"

    return f"login error: {error}"

@bp.route('/logout')
def logout():
    session.clear()
    return "User has been logged out"

@bp.route('/register', methods=('POST',))
def register():
    username = request.form['username']
    password = request.form['password']
    db = get_db()
    error = None
        
    if not username:
        error = 'Username is required.'
    elif not password:
        error = 'Password is required.'

    if error is None:
        try:
            db.execute(
                "INSERT INTO user (username, password) VALUES (?, ?)",
                (username, generate_password_hash(password)),
            )
            db.commit()
            return f"User was created successfully"
        except db.IntegrityError:
            error = f"User {username} is already registered."

    return f"Error creating user: {error}"
