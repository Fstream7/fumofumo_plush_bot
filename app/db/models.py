from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship
from .base import Base


class Fumo(Base):
    __tablename__ = "fumo"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
    file_id = Column(String, unique=True)
    source_link = Column(String, nullable=True)
    use_for_quiz = Column(Boolean, default=False)


class QuizUsers(Base):
    __tablename__ = "quiz_users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Float)
    fumo_name = Column(String, ForeignKey("fumo.name"), nullable=False)
    fumo_count = Column(Integer, default=0)

    fumo = relationship("Fumo", backref="quiz_entries")
