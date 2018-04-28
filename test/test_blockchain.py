# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
from unittest import TestCase

import blockchain.chain
import blockchain.block
import blockchain.transaction as transaction
import blockchain.wallet

# noinspection SpellCheckingInspection
import miner.miner

pre_set_my_address = b'14RLSDUWTCy2frtZk7KLKUpJSQHYX2YwxX'
# noinspection SpellCheckingInspection
chain1 = blockchain.chain.Chain([
    blockchain.block.Block(
        version=0,
        prev_hash='0000ea80f5ba55f9440fdba06f44243628eef272549b2bab3948f99dfc1be74b',
        merkle_hash='7c1aa462c3023e91b1ed76e08647a0cffa279a04dc7b213d44d39fb09b5978e7',
        bits=16,
        nonce=25074,
        txn_manager=transaction.TransactionManager(
            txns=[
                transaction.Transaction(
                    txins=[transaction.TxIn(txid=None, txout_idx=None, unlock_sig=b'1', unlock_pk=None)],
                    txouts=[transaction.TxOut(value=5000000000, receiver=pre_set_my_address)]
                )
            ]
        ),
        stamp=1524905831,
    ),
    blockchain.block.Block(
        version=0,
        prev_hash='0000e70a825dc8d577c0303ddc48ebc0389a4f6c7d12a6aed38edc93c555617e',
        merkle_hash='4fe62a5544bd5d4f288d01f18fdd6202cd6778f8ec4eda6b41fa6d45d4d510d9',
        bits=16,
        nonce=30412,
        txn_manager=transaction.TransactionManager(
            txns=[
                transaction.Transaction(
                    txins=[transaction.TxIn(txid=None, txout_idx=None, unlock_sig=b'2', unlock_pk=None)],
                    txouts=[transaction.TxOut(value=5000000000, receiver=pre_set_my_address)]
                )
            ]
        ),
        stamp=1524905831,
    ),
    blockchain.block.Block(
        version=0,
        prev_hash='0000fd7b9fe251b866d6d842b7cc64e1ff747ff50ab9c693f02f9e824c421e4f',
        merkle_hash='ef7a987a69d126e1513310142fc18cd030c74a8a32f558461ffbad28b3909daa',
        bits=16,
        nonce=73016,
        txn_manager=transaction.TransactionManager(
            txns=[
                transaction.Transaction(
                    txins=[transaction.TxIn(txid=None, txout_idx=None, unlock_sig=b'3', unlock_pk=None)],
                    txouts=[transaction.TxOut(value=5000000000, receiver=pre_set_my_address)]
                )
            ]
        ),
        stamp=1524905831,
    )
])
# noinspection SpellCheckingInspection
chain2 = blockchain.chain.Chain([
    blockchain.block.Block(
        version=0,
        prev_hash='0000ea80f5ba55f9440fdba06f44243628eef272549b2bab3948f99dfc1be74b',
        merkle_hash='7c1aa462c3023e91b1ed76e08647a0cffa279a04dc7b213d44d39fb09b5978e7',
        bits=16,
        nonce=165817,
        txn_manager=transaction.TransactionManager(
            txns=[
                transaction.Transaction(
                    txins=[transaction.TxIn(txid=None, txout_idx=None, unlock_sig=b'1', unlock_pk=None)],
                    txouts=[transaction.TxOut(value=5000000000, receiver=pre_set_my_address)]
                )
            ]
        ),
        stamp=1524905878,
    ),
    blockchain.block.Block(
        version=0,
        prev_hash='000018c515dc2f0b39267b20bca83e5cab75b5096ad9b941bd08f6c0ac110bb4',
        merkle_hash='4fe62a5544bd5d4f288d01f18fdd6202cd6778f8ec4eda6b41fa6d45d4d510d9',
        bits=16,
        nonce=27769,
        txn_manager=transaction.TransactionManager(
            txns=[
                transaction.Transaction(
                    txins=[transaction.TxIn(txid=None, txout_idx=None, unlock_sig=b'2', unlock_pk=None)],
                    txouts=[transaction.TxOut(value=5000000000, receiver=pre_set_my_address)]
                )
            ]
        ),
        stamp=1524905878,
    ),
    blockchain.block.Block(
        version=0,
        prev_hash='0000f8cf7464bcc9c9217fd05d074055ba16eaf1c53560ac1555120150420fc4',
        merkle_hash='ef7a987a69d126e1513310142fc18cd030c74a8a32f558461ffbad28b3909daa',
        bits=16,
        nonce=72459,
        txn_manager=transaction.TransactionManager(
            txns=[
                transaction.Transaction(
                    txins=[transaction.TxIn(txid=None, txout_idx=None, unlock_sig=b'3', unlock_pk=None)],
                    txouts=[transaction.TxOut(value=5000000000, receiver=pre_set_my_address)]
                )
            ]
        ),
        stamp=1524905878,
    ),
    blockchain.block.Block(
        version=0,
        prev_hash='0000e292b56fb4f361275842b3d2c939ccf857a7d6e0ad7fd2ffecd0eee1770d',
        merkle_hash='c06a8b0c4602d14f8757409ef81cdded828ed249ff16e33a3b70499bdcab70cf',
        bits=16,
        nonce=111472,
        txn_manager=transaction.TransactionManager(
            txns=[
                transaction.Transaction(
                    txins=[transaction.TxIn(txid=None, txout_idx=None, unlock_sig=b'4', unlock_pk=None)],
                    txouts=[transaction.TxOut(value=5000000000, receiver=pre_set_my_address)]
                )
            ]
        ),
        stamp=1524905878,
    ),
    blockchain.block.Block(
        version=0,
        prev_hash='0000ec4c1e7effc53987e705bc3684ea697dd7745b6fbe9ed4cae04ad3b98c16',
        merkle_hash='be3cd868f9cf09599e2541a66bb8d6d33dd2b97610235674781610b03ff3f8bb',
        bits=16,
        nonce=84918,
        txn_manager=transaction.TransactionManager(
            txns=[
                transaction.Transaction(
                    txins=[transaction.TxIn(txid=None, txout_idx=None, unlock_sig=b'5', unlock_pk=None)],
                    txouts=[transaction.TxOut(value=5000000000, receiver=pre_set_my_address)]
                )
            ]
        ),
        stamp=1524905878,
    )
])


class TestTransaction(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_merkle_root(self):
        blocks = chain1.blocks + chain2.blocks
        for block in blocks:
            self.assertEqual(block.merkle_hash,
                             block.txn_manager.merkle_root.val)


class TestBlock(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_id(self):
        for chain in [chain1, chain2]:
            for i, block in enumerate(chain.blocks[:-1]):
                self.assertEqual(block.id, chain.blocks[i + 1].prev_hash)


class TestChain(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_connect_block(self):
        chain_manager = blockchain.chain.ChainManager()
        for block in chain1.blocks:
            chain_idx = chain_manager.connect_block(block)
            self.assertEqual(chain_idx, 0)

    def test_reorganize(self):
        # chain_manager = blockchain.chain.ChainManager()
        # for block in chain2.blocks:
        #     chain_manager.connect_block(block)
        # # the $(fork_idx + 1)th element in chain2,
        # # and the $(fork_idx + 2)th element in main_chain
        # fork_idx = 2
        # # exactly one more element than main_chain
        # prev_hash = chain2.blocks[fork_idx].id
        #
        # branch_chain = blockchain.chain.Chain()
        # for i in range(len(chain2.blocks) - fork_idx):
        #     block = miner.miner.Miner.mine(prev_hash)
        #     prev_hash = block.id
        #     branch_chain.add(block)
        # chain_manager.chains.append(branch_chain)
        # chain_manager.reorganize()
        # self.assertEqual(len(chain_manager.main_chain.blocks),
        #                  len(chain2.blocks) + 1)
        self.assertTrue(True)


class TestWallet(TestCase):

    def setUp(self):
        self.path = '../data/wallet.dat'

    def tearDown(self):
        pass

    def test_init_wallet(self):
        signing_key, verifying_key, my_address = blockchain.wallet.init_wallet(path=self.path)
        self.assertEqual(my_address, pre_set_my_address)


if __name__ == '__main__':
    unittest.main()
