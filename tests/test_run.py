from tests import BaseTestCase


class TestRun(BaseTestCase):
    def test_app_get(self):
        response = self.client.get('/')
        self.assert200(response)
