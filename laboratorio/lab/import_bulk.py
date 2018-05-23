import csv
import os
import sqlite3
import sys
from collections import namedtuple
from datetime import datetime

BASE_PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(BASE_PROJECT)

os.environ['DJANGO_SETTING_MODULE'] = 'laboratorio.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "laboratorio.settings")

import django

django.setup()

from django.contrib.auth.models import User
from laboratorio.lab.models import Toronto311

from laboratorio.lab.timeit import timeit

from laboratorio.lab.model_sqlalchemy import Toronto311_Alchemy


class Handling:

    def __init__(self):
        self.owner = User.objects.get(pk=1)
        self.BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    @timeit
    def sql_raw(self):

        conn = sqlite3.connect(os.path.join(self.BASEDIR, '../db.sqlite3'))

        conn.isolation_level = "EXCLUSIVE"
        cursor = conn.cursor()

        cursor.execute("PRAGMA cache_size = 3096")
        cursor.execute("PRAGMA synchronous = OFF")
        cursor.execute("PRAGMA journal_mode = MEMORY")

        carga_insert = []

        sql_insert = """
                        INSERT INTO lab_toronto311(owner_id, creation_date, status, first_3_chars_of_postal_code,
                        intersection_street_1, intersection_street_2, ward, service_request_type, division, section)
                        VALUES(?,?,?,?,?,?,?,?,?,?)
                     """

        data = None
        with open(self.BASEDIR + '/lab/files/SR2017.csv', newline="") as infile:
            reader = csv.reader(infile)
            toronto = namedtuple("toronto", next(reader))

            for data in map(toronto._make, reader):
                carga_insert.append((self.owner.id,
                                     data.Creation_Date,
                                     data.Status,
                                     data.First_3_Chars_of_Postal_Code,
                                     data.Intersection_Street_1,
                                     data.Intersection_Street_2,
                                     data.Ward,
                                     data.Service_Request_Type,
                                     data.Division,
                                     data.Section))

                """    
                toronto(Creation_Date='2017-01-01 00:10:19.0000000', 
                        Status='Closed',
                        First_3_Chars_of_Postal_Code='M9A', 
                        Intersection_Street_1='', 
                        Intersection_Street_2='',
                        Ward='Etobicoke Centre (04)', 
                        Service_Request_Type='Noise',
                        Division='Municipal Licensing & Standards', 
                        Section='District Enforcement')
                """

        if carga_insert:
            try:
                print('Insert SQL RAW...')

                cursor.executemany(sql_insert, carga_insert)
                conn.commit()
                conn.close()

            except BaseException as er:
                print(er, data)

    @timeit
    def orm_django_bulk(self):

        carga_insert = []

        data = None
        with open(self.BASEDIR + '/lab/files/SR2017.csv', newline="") as infile:
            reader = csv.reader(infile)
            toronto = namedtuple("toronto", next(reader))

            for data in map(toronto._make, reader):
                self.dt_creation = data.Creation_Date

                # if data.Creation_Date:
                #     self.dt_creation = datetime.strptime(data.Creation_Date,
                #                                           "%Y-%m-%d %H:%M:%S.0000000").strftime('%Y-%m-%d %H:%M:%S.0000000')

                carga_insert.append((Toronto311(owner_id=self.owner.id,
                                                creation_date=self.dt_creation,
                                                status=data.Status,
                                                first_3_chars_of_postal_code=data.First_3_Chars_of_Postal_Code,
                                                intersection_street_1=data.Intersection_Street_1,
                                                intersection_street_2=data.Intersection_Street_2,
                                                ward=data.Ward,
                                                service_request_type=data.Service_Request_Type,
                                                division=data.Division,
                                                section=data.Section)))
        if carga_insert:
            print("Insert ORM DJANGO BULK...")
            Toronto311.objects.bulk_create(carga_insert)

    @timeit
    def orm_django(self):

        data = None
        carga_insert = []

        with open(self.BASEDIR + '/lab/files/SR2017.csv', newline="") as infile:
            reader = csv.reader(infile)
            toronto = namedtuple("toronto", next(reader))

            for data in map(toronto._make, reader):

                if data.Creation_Date:
                    self.dt_creation = datetime.strptime(data.Creation_Date,
                                                         "%Y-%m-%d %H:%M:%S.0000000").strftime(
                        '%Y-%m-%d %H:%M:%S.0000000')

                Toronto311.objects.create(owner_id=self.owner.id,
                                          creation_date=self.dt_creation,
                                          status=data.Status,
                                          first_3_chars_of_postal_code=data.First_3_Chars_of_Postal_Code,
                                          intersection_street_1=data.Intersection_Street_1,
                                          intersection_street_2=data.Intersection_Street_2,
                                          ward=data.Ward,
                                          service_request_type=data.Service_Request_Type,
                                          division=data.Division,
                                          section=data.Section)

        print("Insert ORM DJANGO...")

    @timeit
    def sqlalchemy_bulk_insert(self):
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker

        BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        dbPath = os.path.join(BASEDIR, '../db.sqlite3')

        engine = create_engine('sqlite:///%s' % dbPath)

        carga_insert = []

        data = None
        with open(self.BASEDIR + '/lab/files/SR2017.csv', newline="") as infile:
            reader = csv.reader(infile)
            toronto = namedtuple("toronto", next(reader))

            for data in map(toronto._make, reader):
                carga_insert.append(Toronto311_Alchemy(owner=self.owner.id,
                                                       creation_date=data.Creation_Date,
                                                       status=data.Status,
                                                       first_3_chars_of_postal_code=data.First_3_Chars_of_Postal_Code,
                                                       intersection_street_1=data.Intersection_Street_1,
                                                       intersection_street_2=data.Intersection_Street_2,
                                                       ward=data.Ward,
                                                       service_request_type=data.Service_Request_Type,
                                                       division=data.Division,
                                                       section=data.Section))

            """    
                toronto(Creation_Date='2017-01-01 00:10:19.0000000', 
                        Status='Closed',
                        First_3_Chars_of_Postal_Code='M9A', 
                        Intersection_Street_1='', 
                        Intersection_Street_2='',
                        Ward='Etobicoke Centre (04)', 
                        Service_Request_Type='Noise',
                        Division='Municipal Licensing & Standards', 
                        Section='District Enforcement')
                """

        if carga_insert:
            print('Insert SQL RAW...')

            Session = sessionmaker(bind=engine)
            session = Session()

            session.bulk_save_objects(carga_insert)

            session.commit()
            session.close()


if __name__ == '__main__':
    handle = Handling()

    handle.sql_raw()
    # handle.orm_django_bulk()
    # handle.sqlalchemy_bulk_insert()

    # handle.orm_django() # Não executar novamente, pelo amor de Deus...

"""

INSERT DE 396.379 registros


Insert SQL RAW... 
'sql_raw' 6.208 s

Insert ORM DJANGO...
'orm_django' 53.343 s s

Insert ORM DJANGO...
'orm_django' 5005.185 s

Insert ORM SqlAlchemy...
'sqlalchemy_bulk_insert' 31.947 s

-------------------------------------------------------------
-------------------------------------------------------------
INSERÇÃO EM SEQUÊNCIA...

Insert SQL RAW...
'sql_raw' 6.345 s

Insert ORM DJANGO BULK...
'orm_django_bulk' 68.766 s

Insert SQL RAW...
'sqlalchemy_bulk_insert' 39.401 s

"""
