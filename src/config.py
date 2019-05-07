import os
basedir = os.path.abspath(os.path.dirname(__file__))

selected_config = 'production'

if selected_config != 'production':
    os.environ['DATABASE_URL'] = 'postgresql://filex:files@localhost/files'


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    STATIC_FOLDER = '/templates/static'


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
