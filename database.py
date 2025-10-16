from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker

SQLITE_DB_URL = "sqlite:///./catalog.db"
db_connect_engine = create_engine(
    SQLITE_DB_URL, connect_args={"check_same_thread": False}
)
AppSession = sessionmaker(autocommit=False, autoflush=False, bind=db_connect_engine)
OrmBase = declarative_base()