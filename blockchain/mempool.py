# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import blockchain.transaction
import server.encoder as encoder
import server.peer
import utils.error

from blockchain.settings import *
from utils import singleton


@singleton
class Mempool:

    def __init__(self):
        self.pool = {}
        self.orphan_txns = []

    def find_utxo(self, txin):
        # noinspection PyBroadException
        try: txout = self.pool[txin.txid].txouts[txin.txout_idx]
        except Exception: return None
        return blockchain.transaction.UTxOut(*txout, txin.txid, txin.txout_idx, False, -1)

    def add_transaction(self, txn):
        peer_manager = server.peer.PeerManager()

        if txn.id in self.pool:
            return None

        try: txn.validate()
        except utils.error.TxValidationError as e:
            if e.to_orphan: self.orphan_txns.append(e.to_orphan)
        else:
            self.pool[txn.id] = txn
            peer_manager.notify_all_peers(encoder.encode_http_data(txn))

    def get_transaction(self, txid):
        if txid not in self.pool:
            raise ValueError('Wrong transaction id')
        return self.pool[txid]

    def del_transaction(self, txid):
        if txid not in self.pool: return None
        del self.pool[txid]

    def transaction_iter(self):
        for txid in self.pool:
            if isinstance(txid, tuple): continue
            yield txid

    def load_transactions(self, block):
        utxo_manager = blockchain.transaction.UTXOManager()

        def add_to_block(_txid):
            if _txid in added_to_block:
                return None

            txn = self.get_transaction(_txid)
            for txin in txn.txins:
                if utxo_manager.find(_txid, txin.txout_idx): continue
                utxo = self.find_utxo(txin)
                if not utxo: return None
                add_to_block(utxo.txid)
                if not block: return None
            if len(block.txn_manager.txns) < MAX_BLOCK_SIZE:
                block.txn_manager.txns.append(txn)
                added_to_block.add(_txid)

        added_to_block = set()
        for txid in self.transaction_iter():
            if len(block.txn_manager.txns) < MAX_BLOCK_SIZE:
                add_to_block(txid)

        return block
