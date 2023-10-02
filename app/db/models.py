from sqlalchemy import Column, String, BigInteger, DateTime, Text, Integer, ForeignKey
import pytz
from db.base import Base
from config import Config


class media_users(Base):
    __tablename__ = "media_users"

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, unique=True, autoincrement=False)
    username = Column(String)
    date_added = Column(DateTime)

    def __repr__(self):
        desired_timezone = pytz.timezone(Config.TZ)
        return f"id: {self.id}, user_id: {self.user_id}, username: {self.username}, date added: {self.timestamp_column.astimezone(desired_timezone)}"


class media(Base):
    __tablename__ = "media"

    id = Column(Integer, primary_key=True)
    media_type = Column(String)
    media_file_id = Column(BigInteger)
    user_id = Column(Integer, ForeignKey("media_users.user_id"))
    date_added = Column(DateTime)

    def __repr__(self):
        desired_timezone = pytz.timezone(Config.TZ)
        return f"id: {self.id}, media_type: {self.media_type}, media_file_id: {self.media_file_id}, user_id: {self.user_id}, date added: {self.timestamp_column.astimezone(desired_timezone)}"


class phrases(Base):
    __tablename__ = "phrases"
    id = Column(Integer, primary_key=True)
    phrase_type = Column(String)
    phrase = Column(Text)
    date_added = Column(DateTime)
