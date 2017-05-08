import os


class Config(object):
    BASE_PATH = os.path.abspath(os.path.dirname(__file__))  # Define the application directory
    TEST_KEY = 'QQBx4jTpQK2CzadBK96hnqZXkfPxMvk4G7GM3kQvy'
    AWS_ACCESS_KEY_ID = ''
    AWS_SECRET_ACCESS_KEY = ''
    SECRET_KEY = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    REDIS_IP = ''
    DATABASE = 'sqeezer'
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
