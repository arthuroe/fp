from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

from api import app


db = SQLAlchemy()


class ModelMixin(db.Model):
    """Base models.

    - Contains the serialize method to convert objects to a dictionary
    - Save and Delete utilities
    - Common field atrributes in the models
    """

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    def serialize(self):
        """Map model objects to dict representation."""
        return {column.name: getattr(self, column.name)
                for column in self.__table__.columns}

    def save(self):
        """Save an instance of the model to the database."""
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except SQLAlchemyError:
            db.session.rollback()
            return False

    @classmethod
    def fetch_all(cls):
        """Return all the data in the model."""
        return cls.query.all()

    @classmethod
    def filter_by(cls, **kwargs):
        """Query and filter the data of the model."""
        return cls.query.filter_by(**kwargs)

    @classmethod
    def find_first(cls, **kwargs):
        """Query and filter the data of a model, returning the first result."""
        return cls.query.filter_by(**kwargs).first()

    @classmethod
    def count(cls):
        """Return the count of all the data in the model."""
        return cls.query.count()

    @classmethod
    def filter(cls, *args):
        """Query and filter the data of the model."""
        return cls.query.filter(*args)
