import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from project_store_config_layer.configuration import Configuration
from project_store_exception_layer.exception import CustomException as DatabaseException

try:
    SQLALCHEMY_DATABASE_URI = Configuration().HOST

    engine = create_engine(SQLALCHEMY_DATABASE_URI,
                        connect_args={'check_same_thread': False}
                        )

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()

except Exception as e:
    load_db_exception = DatabaseException(
    "Failed during loading Database file in module")
    raise Exception(load_db_exception.error_message_detail(str(e), sys))\
            from e