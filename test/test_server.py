# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
from unittest import TestCase
import server.encoder
import blockchain.block
import blockchain.transaction


block = blockchain.block.Block(
    version=0,
    prev_hash=None,
    merkle_hash='12ad3b02b649ff3c202119cd13121281f6e865a24953bc1b99cabea3877fa45d',
    bits=16,
    nonce=55214,
    txn_manager=blockchain.transaction.TransactionManager(
        txns=[blockchain.transaction.Transaction(
            txins=[blockchain.transaction.TxIn(
                txid=None,
                txout_idx=None,
                unlock_sig=b'0',
                unlock_pk=None
            )],
            txouts=[blockchain.transaction.TxOut(
                value=5000000000,
                receiver=b'19N124Bykfao6v2cBN3Ub4xTW6eMWv3SHS'
            )]
        )],
    ),
    stamp=1524900853,
)


class TestEncoder(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_encode_http_data(self):
        # txn = block.txn_manager.txns[0]
        # txn_data = """{'txins': [{'unlock_pk': None, 'unlock_sig': b'0', 'txid': None, 'txout_idx': None}], 'txouts': [{'value': 5000000000, 'receiver': b'19N124Bykfao6v2cBN3Ub4xTW6eMWv3SHS'}], 'type': 'transaction'}"""
        # self.assertEqual(server.encoder.encode_http_data(txn), txn_data)
        # TODO: transform from dict to ordereddict or can not be compared
        pass

    def test_decode_http_data(self):
        def txn_equal(txn1, txn2):
            for j, txin in enumerate(txn1.txins):
                if txin != txn2.txins[j]:
                    return False
            for j, txout in enumerate(txn1.txouts):
                if txout != txn2.txouts[j]:
                    return False
            return True

        global block
        origin_txn = block.txn_manager.txns[0]
        txn_data = server.encoder.encode_http_data(origin_txn)
        rec_txn = server.encoder.decode_http_data(txn_data)
        self.assertTrue(txn_equal(origin_txn, rec_txn))

        origin_block = block
        block_data = server.encoder.encode_http_data(block)
        rec_block = server.encoder.decode_http_data(block_data)
        self.assertEqual(origin_block.version, rec_block.version)
        self.assertEqual(origin_block.prev_hash, rec_block.prev_hash)
        self.assertEqual(origin_block.merkle_hash, rec_block.merkle_hash)
        self.assertEqual(origin_block.bits, rec_block.bits)
        self.assertEqual(origin_block.nonce, rec_block.nonce)
        self.assertEqual(origin_block.stamp, rec_block.stamp)
        for i, tx1 in enumerate(origin_block.txn_manager.txns):
            self.assertTrue(txn_equal(tx1, rec_block.txn_manager.txns[i]))


if __name__ == '__main__':
    unittest.main()
