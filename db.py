from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime

Base = declarative_base()
engine = create_engine("sqlite:///chatbot.db", echo=False)
Session = sessionmaker(bind=engine)
session = Session()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    chats = relationship("Chat", back_populates="user")

class Chat(Base):
    __tablename__ = "chats"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String, default="New Chat")
    messages = relationship("Message", back_populates="chat")
    user = relationship("User", back_populates="chats")

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, ForeignKey("chats.id"))
    role = Column(String)
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.now)
    chat = relationship("Chat", back_populates="messages")

Base.metadata.create_all(engine)