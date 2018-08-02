""" This module defines the models mapped on the database """
import json
from sqlalchemy import create_engine, Column
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import TEXT, INTEGER
from config import CURRENT_CONFIG


MODEL = declarative_base()


class Report(MODEL):
    """ An abstract report structure """
    __tablename__ = "reports"

    id = Column(INTEGER, primary_key=True)
    type = Column(TEXT)

    def to_dict(self):
        """ Converts the .text attribute to json """
        return json.loads(self.type)


def get_engine(
    proto,
    username,
    password,
    host,
    dbname
):
    """ creates the db connection """
    return create_engine(
        "{}://{}:{}@{}/{}".format(
            proto,
            username,
            password,
            host,
            dbname
        ),
        encoding="utf-8"
    )


def initialize_database():
    """ Initializes the database if not initialized already """
    engine = get_engine(
        CURRENT_CONFIG.DB_PROTOCOL,
        CURRENT_CONFIG.DB_USERNAME,
        CURRENT_CONFIG.DB_PASSWORD,
        CURRENT_CONFIG.DB_HOSTNAME,
        CURRENT_CONFIG.DB_DATABASE
    )
    MODEL.metadata.create_all(engine)
    return engine


def get_session():
    """ Get the SA session """
    engine = get_engine(
        CURRENT_CONFIG.DB_PROTOCOL,
        CURRENT_CONFIG.DB_USERNAME,
        CURRENT_CONFIG.DB_PASSWORD,
        CURRENT_CONFIG.DB_HOSTNAME,
        CURRENT_CONFIG.DB_DATABASE
    )
    SessionClass = sessionmaker(bind=engine)
    session = SessionClass()
    return session
