# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from peewee import *

from model.base import BaseModel
from model.block import Block


class Transaction(BaseModel):
    block = ForeignKeyField(Block, related_name='txns')


class TxIn(BaseModel):
    txn = ForeignKeyField(Transaction, related_name='txins')
    txid = CharField(default='', max_length=64)
    txout_idx = IntegerField(default=0)
    unlock_sig = CharField(default='', max_length=64)
    unlock_pk = CharField(default='', max_length=64)


class TxOut(BaseModel):
    txn = ForeignKeyField(Transaction, related_name='txouts')
    value = IntegerField(default=0)
    receiver = CharField(default='', max_length=64)
