from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func

from .bdCreator import Base

class Unreads(Base):
    __tablename__ = 'unreads'

    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    url = Column(String)
    profile_id = Column(Integer, ForeignKey("profiles.id"))
    on_created = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, user_id, url, profile_id):
        self.user_id = user_id
        self.profile_id = profile_id
        self.url = url

    def get_list(self):
        return [self.id, self.user_id, self.url, self.profile_id, self.on_created]
