from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://test:test@localhost:3306/fastapi_sample?charset=utf8"
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Sessionが生成できなかった場合はエラーとする
if Session is None:
    raise Exception("Session is None")

session = Session()