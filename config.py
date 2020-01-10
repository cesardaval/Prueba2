import os


class Config(object):
    """docstring for Config"""
    SECRET_KEY = "lnsaldkaksd"


class Configuracion_desarrollo(Config):
    DEBUG = True
    PORT = 7000
    #SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:proquinteroXDXD@localhost/Prueba3'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///databases/Prueba3.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    