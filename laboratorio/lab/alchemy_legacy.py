import os
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import mapper, sessionmaker

from pprint import pprint


class Toronto311(object):
    pass


# ----------------------------------------------------------------------
def loadSession():
    """"""
    BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dbPath = os.path.join(BASEDIR, '../db.sqlite3')

    engine = create_engine('sqlite:///%s' % dbPath, echo=True)

    metadata = MetaData(engine)
    lab_toronto311 = Table('lab_toronto311', metadata, autoload=True)
    mapper(Toronto311, lab_toronto311)

    Session = sessionmaker(bind=engine)
    session = Session()

    print(Toronto311)

    return session


if __name__ == "__main__":
    session = loadSession()
    res = session.query(Toronto311).all()

    pprint(res[1].ward)