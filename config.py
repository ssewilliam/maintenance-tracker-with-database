class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = "the very secret of secrets"


class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_URL = "postgresql://postgres:password@localhost:5432/trackerdb_dev"


class ProductionConfig(Config):
    DEBUG = False
    DATABASE_URL = "postgresql://postgres:password@localhost:5432/trackerdb"


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    DATABASE_URL = "postgresql://postgress:password@localhost:5432/trackerdb"
