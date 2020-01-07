import os


class Config:
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///hivery.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Large overhead if kept - not required
    RESTPLUS_MASK_SWAGGER = False  # Remove X-mask fields on flask_restplus swagger page
    ERROR_404_HELP = False  # Remove url suggestions when trying to abort with a 404

    # User defined
    RESOURCES_DIR = 'resources'


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'  # In-memory for testing

    RESOURCES_DIR = os.path.join('hivery', 'tests', 'data')


class ProductionConfig(Config):
    pass


config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}
