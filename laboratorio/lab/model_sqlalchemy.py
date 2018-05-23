import os

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DATETIME
from sqlalchemy.ext.declarative import declarative_base

BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dbPath = os.path.join(BASEDIR, '../db.sqlite3')

engine = create_engine('sqlite:///%s' % dbPath, echo=True)

Base = declarative_base()


class Toronto311_Alchemy(Base):
    __tablename__ = "toronto311_alchemy"

    id = Column('id', Integer, primary_key=True)
    owner = Column('owner', Integer)
    creation_date = Column('creation_date', String)
    status = Column('status', String)
    first_3_chars_of_postal_code = Column('first_3_chars_of_postal_code', String)
    intersection_street_1 = Column('intersection_street_1', String)
    intersection_street_2 = Column('intersection_street_2', String)
    ward = Column('ward', String)
    service_request_type = Column('service_request_type', String)
    division = Column('division', String)
    section = Column('section', String)

Base.metadata.create_all(bind=engine)
