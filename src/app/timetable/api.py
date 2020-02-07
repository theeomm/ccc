from flask import request, jsonify
from flask.views import MethodView

from app import db
from app.utils import errorResponse
from .schema import (
    Class,
    ClassSchema,
    Session,
    SessionSchema,
    Subject,
    SubjectSchema,
)




class SessionAPI(MethodView):

    def post(self):

        data = request.get_json()
        name = data.get('name', None)
        period = data.get('period', None)

        if name is None or name == "":
            return errorResponse('Session name is required', 400)

        if period is None or period == "":
            return errorResponse('Session period is required', 400)

        session = Session.query.filter_by(name=name).first()

        if session is None:

            # Create a class session
            session = Session(
                name=name,
                period=period
            )

            # Save new class session to database
            db.session.add(session)
            db.session.commit()

            # Return the create session
            return SessionSchema().dump(session), 201

        return errorResponse('Session already exists', 400)

    def get(self, id=None):

        if id is None:
            """
            Fetch all sessions if an id isn't provided
            """

            sessions = Session.query.all()

            return jsonify(SessionSchema(many=True).dump(sessions)), 200

        session = Session.query.get(id)

        # Check if an entry exists with provided ID
        if session is None:
            return errorResponse('Invalid session ID'), 404

        return SessionSchema().dump(session)

    def patch(self, id):
        """
        Update/Modify a session
        """

        data = request.get_json()
        name = data.get('name', None)
        period = data.get('period', None)

        session = Session.query.get(id)

        if session is None:
            return errorResponse('Invalid session ID', 404)

        if name is not None:
            session.name = name

        if period is not None:
            session.period = period

        db.session.commit()

        return SessionSchema().dump(session), 200

    def delete(self, id):
        """
        Delete a session
        """

        session = Session.query.get(id)

        if session is None:
            return errorResponse('Session not found', 404)

        db.session.delete(session)
        db.session.commit()

        return jsonify({
            'message': 'Session deleted successfully'
        }), 200


class ClassAPI(MethodView):

    def post(self):

        data = request.get_json()
        grade = data.get('grade', None)
        year = data.get('year', None)
        subjects = data.get('subjects', None)

        klass = Class(
            grade=grade,
            year=year,
        )

        if subjects is not None:
            klass.subjects = subjects

        db.session.add(klass)
        db.session.commit()

        return ClassSchema().dump(klass)

    def get(self, id=None):

        if id is None:
            klasses = Class.query.all()
            return jsonify(ClassSchema(many=True).dump(klasses))

        klass = Class.query.get(id)

        if klass is None:
            return errorResponse('Class Not Found', 404)

        return ClassSchema().dump(klass)

    def patch(self, id):

        data = request.get_json()
        grade = data.get('grade', None)
        year = data.get('year', None)
        subjects = data.get('subjects', None)

        klass = Class.query.get(id)

        if klass is None:
            return errorResponse('Class Not Found', 404)

        if grade is not None:
            klass.grade = grade

        if year is not None:
            klass.year = year

        if subjects is not None:
            klass.subjects = subjects

        db.session.commit()

        return ClassSchema().dump(klass)

class SubjectAPI(MethodView):

    # CREATE
    def post(self):
        """
        Create/Add a new subject
        """

        data = request.get_json()
        name = data.get('name', None)

        if name is None or name == "":
            return errorResponse('Subject name is required', 400)

        # Check for the subject in the database
        subject = Subject.query.filter_by(name=name).first()

        if subject is None:
            # Create the subject
            subject = Subject(
                name=name
            )

            if 'teachers' in data:
                subject.teachers = data['teachers']

            # Add subject to database
            db.session.add(subject)
            db.session.commit()

            return SubjectSchema().dump(subject), 201

        return errorResponse('Subject already exists in database', 400)

    # READ

    def get(Self, id=None):
        """
        Retrieve all the subjects or just a single subject
        """

        if id is None:
            subjects = Subject.query.all()
            return jsonify(SubjectSchema(many=True).dump(subjects)), 200
        else:
            subject = Subject.query.get(id)

            if subject is None:
                return errorResponse('Invalid subject ID', 404)

            return SubjectSchema().dump(subject), 200

    # UPDATE

    def patch(self, id):
        """
        Update a subject
        """

        data = request.get_json()
        name = data.get('name', None)

        subject = Subject.query.get(id)

        if subject is None:
            return errorResponse('Subject not found', 404)

        if name is not None:
            subject.name = name

            db.session.commit()

            return SubjectSchema().dump(subject)

    # DELETE
    def delete(self, id):
        """
        Delete a subject from the database
        """

        subject = Subject.query.get(id)

        if subject is None:
            return errorResponse('Invalid subject ID', 404)

        #  Delete from database and commit
        db.session.delete(subject)
        db.session.commit()

        return jsonify({
            'message': 'Subject deleted successfully'
        }), 200
