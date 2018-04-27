# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import binascii
import hashlib
from collections import namedtuple

from blockchain import chain_manager, utxo_manager
from blockchain.settings import *
from encrypt import sha, pubkey_to_address, verify
from utils import singleton
from utils.error import TxValidationError, TxUnlockError

TxIn = namedtuple('TxIn', ['txid', 'txout_idx', 'unlock_sig', 'unlock_pk'])
TxOut = namedtuple('TxOut', ['value', 'receiver'])
UTxOut = namedtuple('UTxOut', ['value', 'receiver', 'txid', 'txout_idx',
                               'is_coinbase', 'height'])
MerkleNode = namedtuple('MerkleNode', ['val', 'children'])
TransactionRepr = namedtuple('TransactionRepr', ['txins', 'txouts'])
OutPoint = namedtuple('OutPoint', ['txid', 'txout_id'])


class Transaction:

    def __init__(self, txins, txouts):
        self.txins = txins
        self.txouts = txouts

    @property
    def id(self):
        return hash(self)

    @property
    def is_coinbase(self):
        return len(self.txins) == 1 and self.txins[0].txid is None

    def validate(self):
        if (not self.txouts) or (not self.txins and not self.is_coinbase):
            raise TxValidationError('Missing txouts or txins')

        if sum(txout.value for txout in self.txouts) > MAX_MONEY:
            raise TxValidationError('Spend value too high')

        available_money = 0
        for i, txin in enumerate(self.txins):
            utxo = utxo_manager.find(self.id, txin.txout_idx)
            if not utxo:
                raise TxValidationError('Could not find utxo')
            if len(chain_manager.main_chain) - utxo.height < COINBASE_MATURITY \
                    and utxo.is_coinbase:
                raise TxValidationError('Coinbase utxo not ready for spending')
            try: self.__validate_signature(txin, utxo, self.txouts)
            except TxUnlockError:
                raise TxValidationError('Txin is not a valid spend of utxo')
            available_money += utxo.value
        if available_money < sum(txout.value for txout in self.txouts):
            raise TxValidationError('Spend value is more than available')
        return self

    def __validate_signature(self, txin, utxo, txouts):
        pubkey_as_addr = pubkey_to_address(txin.unlock_pk)
        if pubkey_as_addr != utxo.receiver:
            raise TxUnlockError('public key doesn\'t match')
        spend_msg = self.__build_spend_msg(txin, txouts)
        try:
            verify(txin.unlock_pk, txin.unlock_sig, spend_msg)
        except Exception:
            raise TxUnlockError('Signature doesn\'t match')
        return True

    # noinspection PyMethodMayBeStatic
    def __build_spend_msg(self, txin, txouts):
        _msg = str(OutPoint(txin.txid, txin.txout_idx))
        _msg += binascii.hexlify(txin.unlock_pk).decode()
        _msg += str(txouts)
        return sha(_msg).encode()

    def __repr__(self):
        data = TransactionRepr(self.txins, self.txouts)
        return str(data)

    def __hash__(self):
        return hashlib.sha256(self).hexdigest()

    @staticmethod
    def create_coinbase(receiver, value, height):
        _txins = [TxIn(None, None, str(height).encode(), None)]
        _txouts = [TxOut(value, receiver)]
        return Transaction(_txins, _txouts)


@singleton
class UTXOManager:

    def __init__(self):
        self.utxos = {}

    def add(self, txout, tx, idx, is_coinbase, height):
        utxo = UTxOut(*txout, tx.id, idx, is_coinbase, height)
        op = OutPoint(utxo.txid, utxo.txout_idx)
        self.utxos[op] = utxo

    def remove(self, txid, txout_idx):
        op = OutPoint(txid, txout_idx)
        del self.utxos[op]

    def find(self, txid, txout_idx):
        op = OutPoint(txid, txout_idx)
        return self.utxos[op]


class TransactionManager:

    def __init__(self, txns=None):
        self.txns = txns or []

    @property
    def merkle_root(self):
        def chunk(l, n):
            return (l[i:i + n] for i in range(0, len(l), n))

        def find_root(nodes):
            new_level = [MerkleNode(sha(left.val + right.val), [left, right])
                         for left, right in chunk(nodes, 2)]
            return find_root(new_level) if len(new_level) > 1 else new_level[0]

        leaves = [MerkleNode(sha(txn), None) for txn in self.txns]
        if len(leaves) % 2: leaves.append(MerkleNode(sha(self.txns[-1]), None))
        return find_root(leaves)
