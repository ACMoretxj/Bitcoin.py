# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from peewee import *
from time import time

from blockchain.settings import INITIAL_DIFFICULTY
from model.base import BaseModel


class Block(BaseModel):

    block_id = CharField(default='', max_length=64)
    version = IntegerField(default=0)
    prev_hash = CharField(default='', max_length=64)
    merkle_hash = CharField(default='', max_length=64)
    bits = IntegerField(default=INITIAL_DIFFICULTY)
    nonce = IntegerField(default=0)
    stamp = IntegerField(default=int(time()))
