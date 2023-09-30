from sqlalchemy import Column, Integer, BigInteger

from db.base import Base


class media_users(Base):
    __tablename__ = "media_users"

    user_id = Column(BigInteger, primary_key=True, unique=True, autoincrement=False)
    chat_id = Column(Integer, unique=True, default=0)
