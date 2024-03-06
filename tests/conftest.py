import pytest
from urllib.parse import quote_plus
import sqlalchemy as db
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseSettings


class SqlalchemyTestConfig(BaseSettings):
    DB_IP: str = '0.0.0.0'
    DB_PORT: int = 19163
    DB_USER: str = 'test'
    DB_PWD: str = 'test'
    DB_NAME: str = 'test'
    DB_URL_FORMAT: str = 'postgresql://{0}:{1}@{2}:{3}/{4}'


config = SqlalchemyTestConfig()

db_url = config.DB_URL_FORMAT.format(
    config.DB_USER, quote_plus(config.DB_PWD), config.DB_IP, config.DB_PORT, config.DB_NAME)

engine = db.create_engine(db_url, echo=True)
# connection = engine.connect()
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()
# schema = 'test_schema'
# Base.metadata.schema = schema


@pytest.fixture(scope='function')
def db_session():
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope='function')
def session_obj():
    return Session


def pytest_sessionfinish(session, exitstatus):
    """ whole test run finishes. """
    Base.metadata.drop_all(engine)
