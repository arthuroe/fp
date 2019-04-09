from flask_testing import TestCase

from api import app, app_configuration


class BaseTestCase(TestCase):
    """
    Base test class
    """

    def create_app(self):
        app.config.from_object(app_configuration['testing'])
        return app

    # def setUp(self):
    #     db.create_all()
    #     db.session.commit()
    #
    # def tearDown(self):
    #     db.session.remove()
    #     db.drop_all()
