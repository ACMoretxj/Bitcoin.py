# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from peewee import *


db = MySQLDatabase(database='bitcoin', user='root',
                   passwd='ACMore*123', charset='utf8')


class BaseModel(Model):
    class Meta:
        database = db
