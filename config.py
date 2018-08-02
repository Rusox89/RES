""" Config file """
import os


class SuadeConfig(object):
    """ The SuadeConfig """
    DB_PROTOCOL = "postgres"
    DB_USERNAME = os.getenv('DB_USERNAME') #Hiding those
    DB_PASSWORD = os.getenv('DB_PASSWORD') 
    DB_HOSTNAME = "candidate.suade.org"
    DB_DATABASE = "suade"
    SERVER_NAME = '0.0.0.0:5000'
    DEBUG = True


# Normally I have several configs and this is why I use CURRENT_CONFIG through
# my scripts


CURRENT_CONFIG = SuadeConfig
