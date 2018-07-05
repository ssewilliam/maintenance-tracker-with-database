from base import *

class TestDevelopement(BaseTestCase):
    def test_app_in_developement(self):
        self.assertEqual(
            app.config['DATABASE_URL'], "postgresql://postgres:password@localhost:5432/trackerdb_dev")
        self.assertTrue(app.config['DEBUG'] is True)

class TestProduction(BaseTestCase):
    def production_database(self):
        app.config.from_object("config.ProductionConfig")
        return app.config['DATABASE_URL']

    def test_app_in_production(self):
        self.assertEqual(
            self.production_database(), "postgresql://postgres:password@localhost:5432/trackerdb")
        self.assertTrue(app.config['DEBUG'] is False)
