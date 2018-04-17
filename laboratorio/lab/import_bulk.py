import csv
import os
import sqlite3
import sys
from collections import namedtuple
from pprint import pprint

BASE_PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(BASE_PROJECT)

os.environ['DJANGO_SETTING_MODULE'] = 'laboratorio.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "laboratorio.settings")

import django

django.setup()

from django.contrib.auth.models import User

from laboratorio.lab.timeit import timeit


class Handling:

    def __init__(self):
        self.owner = User.objects.get(pk=1)
        self.BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        print(self.BASEDIR)

        self.conn = sqlite3.connect(os.path.join(self.BASEDIR, '../../db.sqlite3'))

    @timeit
    def sql_raw(self):
        cursor = self.conn.cursor()
        cursor.execute("PRAGMA cache_size = 3096")
        cursor.execute("PRAGMA journal_mode = MEMORY")

        count = 0

        carga_update = []
        carga_insert = []

        sql_insert = """
                     """

        sql_update = """
                     """

        with open(self.BASEDIR + '/lab/files/SR2017.csv', newline="") as infile:
            reader = csv.reader(infile)
            toronto = namedtuple("toronto", next(reader))

            for data in map(toronto._make, reader):
                while count < 10:
                    print(data._asdict())
                    count += 1


                # if self.owner.toronto311_set.filter()




if __name__ == '__main__':
    handle = Handling()
    handle.sql_raw()
