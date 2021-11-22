from flask import Blueprint, request, session
from werkzeug.security import check_password_hash, generate_password_hash

from app import User, db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=('POST',))
def login():
    username = request.form['username']
    password = request.form['password']
    error = None
    user = User.query.filter_by(username=username).first()

    if user is None:
        error = 'Incorrect username.'
    elif not check_password_hash(user.password, password):
        error = 'Incorrect password.'

    if error is None:
        session.clear()
        session['username'] = user.username
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
    error = None
        
    if not username:
        error = 'Username is required.'
    elif not password:
        error = 'Password is required.'

    if error is None:
        try:
            user = User(username, generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            return f"User was created successfully"
        except Exception as e:
            error = e

    return f"Error creating user: {error}"
