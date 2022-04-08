from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
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
    github_url = Column(Integer)
    technology = Column(String)
    owner_username = Column(String, ForeignKey("users.username"))

    owner = relationship("Users", back_populates="todos")