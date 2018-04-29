# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from peewee import prefetch

from blockchain.chain import ChainManager
from model.base import db
from model.block import Block
from model.transaction import Transaction, TxIn, TxOut


def save():
    # TODO: batch save
    saved_blocks = Block.select(Block.block_id)
    chain_manager = ChainManager()
    with db.atomic():
        for block in chain_manager.main_chain.blocks:
            # do not store repeat records
            if block.id in saved_blocks: continue
            block_model = Block()
            block_model.block_id = block.id
            block_model.version = block.version
            block_model.prev_hash = block.prev_hash
            block_model.merkle_hash = block.merkle_hash
            block_model.bits = block.bits
            block_model.nonce = block.nonce
            block_model.stamp = block.stamp
            block_model.save()
            for txn in block.txn_manager.txns:
                txn_model = Transaction()
                txn_model.block = block_model
                txn_model.save()
                for txin in txn.txins:
                    txin_model = TxIn()
                    txin_model.txn = txn_model
                    txin_model.txid = txin.txid
                    txin_model.txout_idx = txin.txout_idx
                    txin_model.unlock_sig = txin.unlock_sig.decode('utf-8')
                    txin_model.unlock_pk = txin.unlock_pk.decode('utf-8')
                    txin_model.save()
                for txout in txn.txouts:
                    txout_model = TxOut()
                    txout_model.txn = txn_model
                    txout_model.value = txout.value
                    txout_model.receiver = txout.receiver.decode('utf-8')
                    txout_model.save()


def recover():
    from blockchain.block import Block as ChainBlock
    from blockchain.transaction import TransactionManager as ChainTxnManager
    from blockchain.transaction import Transaction as ChainTxn
    from blockchain.transaction import TxIn as ChainTxIn
    from blockchain.transaction import TxOut as ChainTxOut
    with db.atomic():
        block_models = prefetch(Block.select(), Transaction.select(),
                                TxIn.select(), TxOut.select())
        for block_model in block_models:
            txn_manager = ChainTxnManager()
            block = ChainBlock(block_model.version, block_model.prev_hash,
                               block_model.merkle_hash, block_model.bits,
                               block_model.nonce, txn_manager,
                               block_model.stamp)
            for txn_model in block_model.txns:
                txins, txouts = [], []
                for txin_model in txn_model.txins:
                    txin = ChainTxIn(txin_model.txid, txin_model.txout_idx,
                                     txin_model.unlock_sig.encode('utf-8'),
                                     txin_model.unlock_pk.encode('utf-8'))
                    txins.append(txin)
                for txout_model in txn_model.txouts:
                    txout = ChainTxOut(txout_model.value,
                                       txout_model.receiver.encode('utf-8'))
                    txouts.append(txout)
                txn = ChainTxn(txins, txouts)
                txn_manager.txns.append(txn)
