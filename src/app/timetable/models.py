from app import db

# Subject to teachers relation table
teacher_subject = db.Table(
    'teacher_subject',
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
    db.Column('subject_id', db.Integer(), db.ForeignKey('subjects.id'))
)

# Class to subjects relation table
class_subjects = db.Table(
    'class_subjects',
    db.Column('class_id', db.Integer(), db.ForeignKey('classes.id')),
    db.Column('subject_id', db.Integer(), db.ForeignKey('subjects.id'))
)


class Class(db.Model):

    __tablename__ = 'classes'

    id = db.Column(db.Integer(), primary_key=True)
    grade = db.Column(db.String(128), index=True)
    year = db.Column(db.String(4))
    subjects = db.relationship(
        'Subject',
        secondary='class_subjects',
        backref=db.backref('subjects', lazy='dynamic')
    )

    def __repr__(self):
        return f"{self.grade} - {self.year}"


class Subject(db.Model):

    __tablename__ = 'subjects'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(128), index=True, unique=True)
    teachers = db.relationship(
        'User',
        secondary='teacher_subject',
        backref=db.backref('teachers', lazy='dynamic',),
    )

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name


class Session(db.Model):

    __tablename__ = 'sessions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Integer())
    period = db.Column(db.String(128), index=True, unique=True)

    def __repr__(self):
        return f"{self.name} - {self.period}"
