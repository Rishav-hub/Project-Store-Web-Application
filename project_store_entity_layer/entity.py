from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import DateTime
from project_store_data_access_layer.data_access import Base

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    todos = relationship("Application", back_populates="owner")

class Application(Base):
    __tablename__ = "application"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    github_url = Column(String)
    technology = Column(String)
    # owner_username = Column(Integer, ForeignKey("users.id"))
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("Users", back_populates="todos")

class LogUser(Base):
    __tablename__ = "log_user"

    id = Column(Integer, primary_key=True, index=True)
    execution_id = Column(String)
    log_writer_id = Column(String)
    status = Column(Boolean)
    log_start_date = Column(String)
    log_start_time = Column(String)
    log_update_time = Column(String)
    log_stop_date = Column(String)
    log_stop_time = Column(String)
    execution_time_milisecond = Column(Integer)
    request = Column(String)
