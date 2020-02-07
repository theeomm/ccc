from app import ma
from .models import Subject, Session, Class

class ClassSchema(ma.ModelSchema):
    """
    Class model schema
    """
    class Meta:
        model = Class

class SubjectSchema(ma.ModelSchema):
    """
    Subject model schema
    """
    class Meta:
        model = Subject


class SessionSchema(ma.ModelSchema):
    """
    Session model schema
    """
    class Meta:
        model = Session
