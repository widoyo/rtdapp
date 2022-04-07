class Config(object):
    TESTING = False


class ProductionConfig(Config):
    DEBUG = False
    DATABASE_URI = ""


class DevelopmentConfig(Config):
    DATABASE_URI = ""


class TestingConfig(Config):
    DATABASE_URI = ""
    TESTING = True
