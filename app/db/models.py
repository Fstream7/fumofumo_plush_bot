from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Fumo(Base):
    __tablename__ = "fumo"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
    file_id = Column(String, unique=True)
    source_link = Column(String, nullable=True)
    use_for_quiz = Column(Boolean, default=False)

    quiz_results = relationship("QuizResults", back_populates="fumo", cascade="all, delete")


class QuizUsers(Base):
    __tablename__ = "quiz_users"

    user_id = Column(Integer, primary_key=True)
    user_name = Column(String, nullable=True)

    quiz_results = relationship("QuizResults", back_populates="quiz_user", cascade="all, delete")


class QuizResults(Base):
    __tablename__ = "quiz_results"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("quiz_users.user_id", ondelete="CASCADE"))
    fumo_id = Column(Integer, ForeignKey("fumo.id", ondelete="CASCADE"))
    fumo_count = Column(Integer, default=0)
    group_id = Column(Integer)

    fumo = relationship("Fumo", back_populates="quiz_results")
    quiz_user = relationship("QuizUsers", back_populates="quiz_results")
