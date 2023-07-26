from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func

from .bdCreator import Base

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    status = Column(Integer)
    on_created = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, status, user_id):
        self.status = status
        self.user_id = user_id

    def get_list(self):
        return [self.id, self.user_id, self.status, self.on_created]