from app import ma
from app.auth.models import User


class UserSchema(ma.ModelSchema):
    """
    User Schema based on the SQLAlchemy User Model
    """
    class Meta:
        model = User
        exclude = ('password', 'last_login_ip', 'current_login_ip')
