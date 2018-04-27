# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import hashlib
from collections import namedtuple
from time import time

from blockchain.blockchain import chain_manager, utxo_manager
from blockchain.settings import *
from utils.error import BlockValidationError, TxValidationError

BlockHeader = namedtuple('BlockHeader',
                         ['version', 'prev_hash', 'merkle_hash',
                          'bits', 'nonce', 'stamp'])


class Block:

    def __init__(self, version, prev_hash, merkle_hash, bits, nonce,
                 txn_manager):
        self.version = version
        self.prev_hash = prev_hash
        self.merkle_hash = merkle_hash
        self.bits = bits
        self.nonce = nonce
        self.txn_manager = txn_manager
        self.stamp = time()

    @property
    def header(self):
        return BlockHeader(self.version, self.prev_hash, self.merkle_hash,
                           self.bits, self.nonce, self.stamp)

    @property
    def id(self):
        return hash(self)

    @property
    def fees(self):
        fee = 0
        for txn in self.txn_manager.txns:
            gain = sum(utxo_manager.find(txn.id, txin.txout_idx)
                       for txin in txn.txins)
            paid = sum(txout.value for txout in txn.txouts)
            fee += gain - paid
        return fee

    def validate(self):
        if not self.txn_manager:
            raise BlockValidationError('Transactions are empty')

        if int(self.id) > (1 << (256 - self.bits)):
            raise BlockValidationError('Block header doesn\'t satisfy bits')

        if {i for i, tx in enumerate(self.txn_manager.txns) if tx.is_coinbase}\
                != {0}:
            raise BlockValidationError('First transaction must be coinbase')

        try:
            for i, txn in enumerate(self.txn_manager.txns):
                txn.validate()
        except TxValidationError:
            raise BlockValidationError('Invalid transaction')

        if self.merkle_hash != self.txn_manager.merkle_root:
            raise BlockValidationError('Merkle hash invalid')

        # TODO timestamp check

        if self.prev_hash or chain_manager.main_chain_idx:
            prev_block, prev_block_height, prev_block_chain_idx = \
                chain_manager.locate_block(self.prev_hash)
            if not prev_block:
                raise BlockValidationError('Previous not found in any chain',
                                           to_orphan=self)
            # this block belongs to side branches
            if prev_block_chain_idx != chain_manager.main_chain_idx:
                return self, prev_block_chain_idx
            # create a new branch
            if prev_block != chain_manager.main_chain[-1]:
                return self, prev_block_chain_idx + 1
        # this is the genesis block
        else: prev_block_chain_idx = MAIN_CHAIN_INDEX

        if Block.next_bits(self.prev_hash) != self.bits:
            raise BlockValidationError('Bits is incorrect')

        for txn in self.txn_manager.txns[1:]:
            try: txn.validate()
            except TxValidationError:
                raise BlockValidationError('Transaction failed to validate')

        return self, prev_block_chain_idx

    def __repr__(self):
        return str(self.header)

    def __hash__(self):
        return hashlib.sha256(self).hexdigest()

    @staticmethod
    def next_bits(prev_hash):
        if not prev_hash:
            return INITIAL_DIFFICULTY
            # TODO
