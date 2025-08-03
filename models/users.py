from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from models.base import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    username = Column(String)
    tg_id = Column(String)
    phone = Column(String)
    role = Column(String)
    command = Column(String)
    docs = relationship("Document", backref="main_user")

    def __repr__(self):
        return f"<User(name:'{self.username}', role:'{self.role}', telegram:'{self.tg_id}')>"
