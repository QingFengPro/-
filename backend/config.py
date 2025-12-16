import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """基础配置"""
    APP_NAME = os.getenv("APP_NAME", "Weibo Sentiment Analysis System")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    SECRET_KEY = os.getenv("SECRET_KEY", "secret-key-change-in-production")

class DatabaseConfig:
    """数据库配置"""
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "mysql+pymysql://root:password@localhost:3306/weibo_sentiment_db"
    )
    SQLALCHEMY_ECHO = os.getenv("SQLALCHEMY_ECHO", "False").lower() == "true"
    POOL_SIZE = 10
    POOL_RECYCLE = 3600

class CrawlerConfig:
    """爬虫配置"""
    CRAWLER_INTERVAL = int(os.getenv("CRAWLER_INTERVAL", "3600"))
    MAX_CONCURRENT_CRAWLERS = int(os.getenv("MAX_CONCURRENT_CRAWLERS", "3"))
    TIMEOUT = 30

class ModelConfig:
    """模型配置"""
    SENTIMENT_MODEL_NAME = os.getenv("SENTIMENT_MODEL_NAME", "bert-base-chinese")
    MODEL_PATH = os.getenv("MODEL_PATH", "./models/sentiment_model")

class APIConfig:
    """API配置"""
    API_TIMEOUT = int(os.getenv("API_TIMEOUT", "30"))
    MAX_REQUEST_SIZE = int(os.getenv("MAX_REQUEST_SIZE", "10485760"))

# 合并所有配置
config = {
    "app": Config,
    "database": DatabaseConfig,
    "crawler": CrawlerConfig,
    "model": ModelConfig,
    "api": APIConfig,
}
