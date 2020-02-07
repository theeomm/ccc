from .models import User
# Flask JWT Utilities


def authenticate(email, password):
    """
    JWT authenticate a user
    """
    user = User.query.filter_by(email=email).first()

    if user is not None:
        if user.check_password(password):
            return user


def identity(payload):
    """
    JWT identity function to identify a user
    """
    user_id = payload['identity']
    return User.query.get(user_id)
