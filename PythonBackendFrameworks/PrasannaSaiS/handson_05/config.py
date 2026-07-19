class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///courses.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'dev-secret-key'
    DEBUG = True
