from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func

from .bdCreator import Base

class Onlines(Base):
    __tablename__ = 'onlines'

    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    user_lvl = Column(Integer)
    user_name = Column(String)
    profile_worked = Column(String, default="")
    count_worked = Column(String, default=0)
    on_created = Column(DateTime(timezone=True), server_default=func.now())
    on_updated = Column(DateTime(timezone=True), onupdate=func.now())

    def __init__(self, user_id, user_lvl, user_name):
        self.user_id = user_id
        self.user_lvl = user_lvl
        self.user_name = user_name

    def get_list(self):
        return [self.id, self.user_id, self.user_lvl, self.user_name, self.profile_worked, self.count_worked, self.on_created, self.on_updated]
