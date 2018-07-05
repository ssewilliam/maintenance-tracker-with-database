class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = "the very secret of secrets"


class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_URL = "postgresql://postgres:password@localhost:5432/trackerdb_dev"


class ProductionConfig(Config):
    DEBUG = False
    DATABASE_URL = "postgres://ipdtvwpzesapxx:cc4530834f4ddb00f1bc61619e59603449c5801aa15ec0740ed90ada0b3349db@ec2-54-83-33-213.compute-1.amazonaws.com:5432/d28f21ref26ahs"


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    DATABASE_URL = "postgresql://postgress:password@localhost:5432/trackerdb"
