import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DB_NAME = os.getenv('DB_NAME')
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_PORT = os.getenv('DB_PORT')
    DB_HOST = os.getenv('DB_HOST')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
