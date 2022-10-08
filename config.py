from logging import DEBUG
import os



class Config(object):
    DEBUG = False
    SECRET_KEY = 'hmssecretkey123'
    SQLALCHEMY_TRACK_MODIFICATIONS = False