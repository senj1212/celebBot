from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import MetaData

engine = create_engine('sqlite:///database.db', convert_unicode=True)

metadata = MetaData()
metadata.reflect(bind=engine)

Session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()



def db_create():
    Base.metadata.create_all(engine)
