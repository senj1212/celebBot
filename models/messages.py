from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from .bdCreator import Base

class Messages(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    status = Column(Integer)
    msg = Column(String)
    profile_id = Column(Integer)
    on_created = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, status, msg, profile_id):
        self.status = status
        self.msg = msg
        self.profile_id = profile_id

    def get_list(self):
        return [self.id, self.status, self.msg, self.profile_id, self.on_created]
