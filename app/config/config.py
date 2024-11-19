class Config:
    DEBUG = True
    # SECRET_KEY = "your_secret_key"
    # SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
    # SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
