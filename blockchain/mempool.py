# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from blockchain.transaction import UTxOut
from server import encode_http_data
from server.peer import PeerManager
from utils import singleton
from utils.error import TxValidationError


@singleton
class Mempool:

    def __init__(self):
        self.mempool = []
        self.orphan_txns = []

    def find_utxo(self, txin):
        # noinspection PyBroadException
        try: txout = self.mempool[txin.txid].txouts[txin.txout_idx]
        except Exception: return None
        return UTxOut(*txout, txin.txid, txin.txout_idx, False, -1)

    def add_transaction(self, txn):
        if txn.id in self.mempool:
            return None

        try: txn.validate()
        except TxValidationError as e:
            if e.to_orphan: self.orphan_txns.append(e.to_orphan)
        else:
            self.mempool[txn.id] = txn
            PeerManager().notify_all_peers(encode_http_data(txn))

    def load_transaction(self, block):
        # TODO
        pass
