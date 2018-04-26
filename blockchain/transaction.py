# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import binascii
import hashlib
from collections import OrderedDict, namedtuple

from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

from blockchain.error import TxValidationError
from blockchain.settings import MAX_MONEY

TxIn = namedtuple('TxIn', ['txid', 'txout_idx', 'unlock_sig', 'unlock_pk'])
TxOut = namedtuple('TxOut', ['value', 'receiver'])
UTxOut = namedtuple('UTxOut', ['value', 'receiver', 'txid', 'txout_idx',
                               'is_coinbase', 'height'])


class Transaction:

    TransactionRepr = namedtuple('TransactionRepr', ['txins', 'txouts'])

    def __init__(self, txins, txouts):
        self.txins = txins
        self.txouts = txouts

    @property
    def id(self):
        return hash(self)

    @property
    def is_coinbase(self):
        return len(self.txins) == 1 and self.txins[0].utxos is None

    def verify(self):
        if (not self.txouts) or (not self.txins and not self.is_coinbase):
            raise TxValidationError('Missing txouts or txins')
        if sum(txout.value for txout in self.txouts) > MAX_MONEY:
            raise TxValidationError('Spend value too high')

    def __repr__(self):
        data = self.TransactionRepr(self.txins, self.txouts)
        return str(data)

    def __hash__(self):
        return hashlib.sha256(self).hexdigest()


class UTXOManager:

    OutPoint = namedtuple('OutPoint', ['txid', 'txout_id'])

    def __init__(self, utxos):
        self.utxos = utxos

    def add(self, txout, tx, idx, is_coinbase, height):
        utxo = UTxOut(*txout, tx.id, idx, is_coinbase, height)
        op = self.OutPoint(utxo.txid, utxo.txout_idx)
        self.utxos[op] = utxo

    def remove(self, txid, txout_idx):
        op = self.OutPoint(txid, txout_idx)
        del self.utxos[op]

    def find(self, txid, txout_idx):
        op = self.OutPoint(txid, txout_idx)
        return self.utxos[op]


class TransactionManager:

    def __init__(self):
        self.transactions = []

    @staticmethod
    def create_coinbase(receiver, value, height):
        _txins = [TxIn(None, None, str(height).encode(), None)]
        _txouts = [TxOut(value, receiver)]
        return Transaction(_txins, _txouts)
