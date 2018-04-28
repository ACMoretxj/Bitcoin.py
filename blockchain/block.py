# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import hashlib
from collections import namedtuple
from time import time

import blockchain.wallet as wallet
import blockchain.mempool
import blockchain.transaction as transaction
import blockchain.chain
from encrypt import sha

from .settings import *
from utils.error import BlockValidationError, TxValidationError


class Block:
    def __init__(self, version, prev_hash, merkle_hash, bits, nonce,
                 txn_manager, stamp=int(time())):
        self.version = version
        self.prev_hash = prev_hash
        self.merkle_hash = merkle_hash
        self.bits = bits
        self.nonce = nonce
        self.txn_manager = txn_manager
        self.stamp = stamp

    @property
    def header(self):
        return '%s%s%s%s%s%s' % (self.version, self.prev_hash,
                                 self.merkle_hash, self.bits,
                                 self.nonce, self.stamp)

    @property
    def id(self):
        return sha(self.header)

    @property
    def fees(self):
        fee, utxo_manager = 0, transaction.UTXOManager()
        for txn in self.txn_manager.txns:
            gain = sum(utxo_manager.find(txn.id, txin.txout_idx)
                       for txin in txn.txins)
            paid = sum(txout.value for txout in txn.txouts)
            fee += gain - paid
        return fee

    def validate(self):
        chain_manager = blockchain.chain.ChainManager()

        if not self.txn_manager:
            raise BlockValidationError('Transactions are empty')

        if int(self.id, 16) > (1 << (256 - self.bits)):
            raise BlockValidationError('Block header doesn\'t satisfy bits')

        if {i for i, tx in enumerate(self.txn_manager.txns) if tx.is_coinbase} \
                != {0}:
            raise BlockValidationError('First transaction must be coinbase')

        try:
            for i, txn in enumerate(self.txn_manager.txns):
                txn.validate()
        except TxValidationError:
            raise BlockValidationError('Invalid transaction')

        if self.merkle_hash != self.txn_manager.merkle_root.val:
            raise BlockValidationError('Merkle hash invalid')

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
            if prev_block != chain_manager.main_chain.blocks[-1]:
                return self, prev_block_chain_idx + 1
        # this is the genesis block
        else:
            prev_block_chain_idx = MAIN_CHAIN_INDEX

        if Block.next_bits(self.prev_hash) != self.bits:
            raise BlockValidationError('Bits is incorrect')

        for txn in self.txn_manager.txns[1:]:
            try:
                txn.validate()
            except TxValidationError:
                raise BlockValidationError('Transaction failed to validate')

        return self, prev_block_chain_idx

    def __repr__(self):
        return str(self.header)

    @staticmethod
    def next_bits(prev_hash):
        chain_manager = blockchain.chain.ChainManager()
        if not prev_hash:
            return INITIAL_DIFFICULTY
        prev_block, prev_height, _ = chain_manager.locate_block(prev_hash)
        if (prev_height + 1) % DIFFICULTY_PERIOD_IN_BLOCKS:
            return prev_block.bits
        period_start_block = chain_manager.main_chain.blocks[
            max(prev_height - DIFFICULTY_PERIOD_IN_BLOCKS + 1, 0)]
        time_used = prev_block.stamp - period_start_block.stamp

        if time_used < DIFFICULTY_PERIOD:
            return prev_block.bits + 1
        elif time_used > DIFFICULTY_PERIOD:
            return prev_block.bits - 1
        return prev_block.bits

    @staticmethod
    def block_subsidy():
        chain_manager = blockchain.chain.ChainManager()
        # noinspection PyBroadException
        try: height = chain_manager.main_chain.height
        except Exception: height = 0
        half_ratio = height // HALF_SUBSIDY_AFTER_BLOCK_NUM
        if half_ratio > MAX_HALF_RATIO: return 0
        return INITIAL_COIN_SUBSIDY * MONEY_PER_COIN // 2 ** half_ratio

    @staticmethod
    def new_block(txns=None, prev_hash=None):
        chain_manager, mempool = blockchain.chain.ChainManager(), blockchain.mempool.Mempool()
        prev_hash = prev_hash or chain_manager.main_chain.blocks[-1].id \
            if chain_manager.main_chain else None
        block = Block(version=0, prev_hash=prev_hash, merkle_hash='',
                      bits=Block.next_bits(prev_hash), nonce=0,
                      txn_manager=transaction.TransactionManager(txns))
        if not block.txn_manager.txns:
            mempool.load_transactions(block)

        my_address = wallet.init_wallet()[2]
        fees = Block.block_subsidy() + block.fees
        # noinspection PyBroadException
        try: height = chain_manager.main_chain.height
        except Exception: height = 0
        coinbase_txn = transaction.Transaction.create_coinbase(my_address, fees, height)
        block.txn_manager.txns.insert(0, coinbase_txn)
        block.merkle_hash = block.txn_manager.merkle_root.val

        if len(block.txn_manager.txns) > MAX_BLOCK_SIZE:
            raise ValueError('too many transactions in a block')

        return block
