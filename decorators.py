from functools import wraps
import flask


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if flask.session.get('user_id'):
            return func(*args, **kwargs)
        else:
            return flask.redirect(flask.url_for('login'))
    return wrapper