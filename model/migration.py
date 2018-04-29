# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from model.block import Block
from model.transaction import Transaction, TxIn, TxOut


if __name__ == '__main__':
    Block.create_table()
    Transaction.create_table()
    TxIn.create_table()
    TxOut.create_table()
