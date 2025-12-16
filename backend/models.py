"""简化的数据模型 - 直接使用 SQLAlchemy ORM"""
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

# 创建基类
Base = declarative_base()

# 初始化数据库引擎
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./weibo_sentiment.db")
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Comment(Base):
    """评论数据模型"""
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)  # 评论内容
    sentiment = Column(String(50), nullable=False)  # 情感：正向/负向/中立
    sentiment_score = Column(Float, default=0.0)  # 情感分值 0-1
    timestamp = Column(DateTime, default=datetime.now)


class Topic(Base):
    """热门话题数据模型"""
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)  # 话题标题
    content = Column(Text, nullable=True)  # 话题内容
    positive_count = Column(Integer, default=0)  # 正向评论数
    negative_count = Column(Integer, default=0)  # 负向评论数
    neutral_count = Column(Integer, default=0)  # 中立评论数
    avg_sentiment_score = Column(Float, default=0.0)  # 平均情感分值
    created_at = Column(DateTime, default=datetime.now)


def init_db():
    """初始化数据库表"""
    Base.metadata.create_all(bind=engine)


def get_db():
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
