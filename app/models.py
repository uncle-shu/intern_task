from sqlalchemy import Column, Integer, String, Enum, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    status = Column(Enum('pending', 'in_progress', 'completed', name='task_status'), default='pending')
    source_language = Column(String)
    target_language = Column(String)
    original_content = Column(Text)
    translated_content = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
