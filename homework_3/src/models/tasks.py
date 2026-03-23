from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from core.database import Base


class Tasks(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(35), nullable=False)
    about = Column(String(100), nullable=True)
    importance = Column(String(20), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    responsible_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    deadline = Column(DateTime(timezone=True), server_default=func.now())
    is_done = Column(Boolean, nullable=False, default=False)
