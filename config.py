import os


class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY', None)


class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_URL = os.getenv('DEVELOPMENT_DATABASE_URL', None)


class ProductionConfig(Config):
    DEBUG = False
    DATABASE_URL = os.getenv('PRODUCTION_DATABASE_URL', None)


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    DATABASE_URL = os.getenv('TEST_DATABASE_URL', None)
