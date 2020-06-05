import json

from datetime import datetime
from flask_testing import TestCase

from api import app, db, app_configuration
from api.models import User


class BaseTestCase(TestCase):
    """
    Base test class
    """

    def create_app(self):
        app.config.from_object(app_configuration['testing'])
        return app

    def setUp(self):
        db.create_all()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def register_user(self, email=None, password=None, first_name=None, is_admin=False):
        return self.client.post(
            '/api/v1/auth/register',
            data=json.dumps(
                dict(email=email, password=password, first_name=first_name)),
            content_type='application/json',
        )

    def login_user(self, email=None, password=None):
        return self.client.post(
            '/api/v1/auth/login',
            data=json.dumps(dict(email=email, password=password)),
            content_type='application/json',
        )

    def create_user(self):
        user = User(email='test@gmail.com',
                    password='tesTing123', first_name='test')
        user.save()
