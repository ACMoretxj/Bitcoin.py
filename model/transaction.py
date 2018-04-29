# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from peewee import *

from model.base import BaseModel
from model.block import Block


class Transaction(BaseModel):
    block = ForeignKeyField(Block, related_name='txns')


class TxIn(BaseModel):
    txn = ForeignKeyField(Transaction, related_name='txins')
    txid = CharField(null=True, max_length=64)
    txout_idx = IntegerField(null=True, default=0)
    unlock_sig = CharField(null=True, max_length=64)
    unlock_pk = CharField(null=True, max_length=64)


class TxOut(BaseModel):
    txn = ForeignKeyField(Transaction, related_name='txouts')
    value = FloatField(default=0)
    receiver = CharField(null=True, max_length=64)
