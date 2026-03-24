"""数据库连接：SQLAlchemy + PostgreSQL"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from config import settings

Base = declarative_base()

# 仅在配置了 DATABASE_URL 时创建引擎
_engine = None
_SessionLocal = None


def get_engine():
    global _engine
    if _engine is None:
        if not settings.DATABASE_URL:
            raise RuntimeError("未配置 DATABASE_URL 环境变量")
        _engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
    return _engine


def get_session():
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(bind=get_engine(), autocommit=False, autoflush=False)
    return _SessionLocal()


def init_db():
    """创建所有表（首次启动时调用）"""
    from models import User, AnalysisRecord  # noqa: F401
    Base.metadata.create_all(bind=get_engine())
