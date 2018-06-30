class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = "the very secret of secrets"


class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_URL = "postgresql://postgres:password@localhost:5432/trackerdb_dev"


class ProductionConfig(Config):
    DEBUG = False
    DATABASE_URL = "postgres://ehbhssmcsvljgt:61e3f44a97a3d0ee9c05ce13d06fe6692fd3186394137a1e2c9d6aae4c3b96c9@ec2-54-235-196-250.compute-1.amazonaws.com:5432/d45koq7e85dqii"


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    DATABASE_URL = "postgresql://postgress:password@localhost:5432/trackerdb2"
