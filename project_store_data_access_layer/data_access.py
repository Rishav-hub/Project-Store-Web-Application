import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from project_store_config_layer.configuration import Configuration
from project_store_exception_layer.exception import CustomException as DatabaseException

def prepare_db():
    try:
        db_config = Configuration()
        db_name = db_config.DB_NAME
        user = db_config.USER
        host = db_config.HOST
        port = db_config.PORT
        password = db_config.PASSWORD

        # password = 'test123'
        database = db_config.DATABASE
        SQLALCHEMY_DATABASE_URI = f"{db_name}://{user}:{password}@{host}:{port}/{database}"
        # SQLALCHEMY_DATABASE_URI = f"{host}"
        engine = create_engine(SQLALCHEMY_DATABASE_URI)
        print("engine Created")
        # curser = engine.connect()
        # curser.execute(f"create database if not exists {db_name}")
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        Base = declarative_base()
        return engine, SessionLocal, Base

    except Exception as e:
        load_db_exception = DatabaseException(
        "Failed during loading Database file in module")
        raise Exception(load_db_exception.error_message_detail(str(e), sys))\
                from e