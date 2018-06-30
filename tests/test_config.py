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
            self.production_database(), "postgres://ehbhssmcsvljgt:61e3f44a97a3d0ee9c05ce13d06fe6692fd3186394137a1e2c9d6aae4c3b96c9@ec2-54-235-196-250.compute-1.amazonaws.com:5432/d45koq7e85dqii")
        self.assertTrue(app.config['DEBUG'] is False)
