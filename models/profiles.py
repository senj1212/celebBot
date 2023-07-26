from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func

from .bdCreator import Base

class Profiles(Base):
    __tablename__ = 'profiles'

    id = Column(Integer, primary_key=True)
    login = Column(String)
    password = Column(String)
    status = Column(Integer, default=0)
    on_created = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, login, password, status):
        self.login = login
        self.password = password
        self.status = status

    def get_list(self):
        return [self.id, self.login, self.password, self.status, self.on_created]
