import os
from base import *

class TestDevelopement(BaseTestCase):
    def test_app_in_developement(self):
        self.assertEqual(
            app.config['DATABASE_URL'], os.getenv('TEST_DATABASE_URL', None))
        self.assertTrue(app.config['DEBUG'] is True)

class TestProduction(BaseTestCase):
    def production_database(self):
        app.config.from_object("config.ProductionConfig")
        return app.config['DATABASE_URL']

    def test_app_in_production(self):
        self.assertEqual(
            self.production_database(), os.getenv('PRODUCTION_DATABASE_URL', None))
        self.assertTrue(app.config['DEBUG'] is False)
