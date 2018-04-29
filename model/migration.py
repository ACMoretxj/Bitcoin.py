# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from model.block import Block
from model.transaction import Transaction, TxIn, TxOut


def create_schema():
    TxIn.drop_table()
    TxOut.drop_table()
    Transaction.drop_table()
    Block.drop_table()

    Block.create_table()
    Transaction.create_table()
    TxIn.create_table()
    TxOut.create_table()


if __name__ == '__main__':
    create_schema()
