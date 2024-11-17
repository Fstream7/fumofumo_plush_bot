from sqlalchemy import Column, String, Integer
from db.base import Base


class Fumo(Base):
    __tablename__ = "fumo"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
    file_id = Column(String, unique=True)
    source_link = Column(String, nullable=True)
