import os
import sys

import csv
import sqlite3
from pprint import pprint
from collections import namedtuple

from unipath import Path as upath

pprint(upath(__file__))

sys.path.append(str(upath(__file__)))

os.environ['DJANGO_SETTING_MODULE'] = 'settings'
import django
django.setup()

from django.contrib.auth.models import User
from laboratorio.lab.models import Toronto311

# from .timeit import timeit

class Test:
    def teste(self):
        print("*"*50)



if __name__ == '__main__':
    teste = Test()
    teste.teste()
    

