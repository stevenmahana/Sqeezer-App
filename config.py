import os


class Config(object):
    BASE_PATH = os.path.abspath(os.path.dirname(__file__))  # Define the application directory
    TEST_KEY = ''
    AWS_ACCESS_KEY_ID = ''
    AWS_SECRET_ACCESS_KEY = ''
    SECRET_KEY = ''
    REDIS_IP = ''
    DATABASE = ''
    DB_USER = ''
    DB_PASS = ''
    REDIS_PORT = 6379
    DEBUG = False
    TESTING = False
    DEVELOPMENT = False
    CSRF_ENABLED = True


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEBUG = True
    DEVELOPMENT = True


class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
