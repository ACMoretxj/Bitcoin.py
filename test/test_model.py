# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
from unittest import TestCase

import blockchain.chain
import miner.miner
from model.base import db
from model.block import Block
from model.migration import create_schema
from model.saver import save, recover


class TestSaver(TestCase):

    def setUp(self):
        create_schema()
        self.new_blocks, self.cnt = [], 3
        chain_manager = blockchain.chain.ChainManager()
        for i in range(self.cnt):
            block = miner.miner.Miner.mine()
            self.assertNotEqual(block, None)
            chain_manager.connect_block(block)
            self.new_blocks.append(block)
        save()

    def tearDown(self):
        stored_block_ids = {bm.block_id for bm in Block.select()}
        new_block_ids = {block.id for block in self.new_blocks}
        with db.atomic():
            for blockid in stored_block_ids & new_block_ids:
                block_model = Block.get(Block.block_id == blockid)
                for txn_model in block_model.txns:
                    for txin_model in txn_model.txins:
                        txin_model.delete_instance()
                    for txout_model in txn_model.txouts:
                        txout_model.delete_instance()
                    txn_model.delete_instance()
                block_model.delete_instance()
        chain_manager = blockchain.chain.ChainManager()
        for block in self.new_blocks[::-1]:
            chain_manager.disconnect_block(block)
        self.new_blocks.clear()

    def test_save(self):
        save()
        chain_manager = blockchain.chain.ChainManager()
        self.assertEqual(chain_manager.main_chain.height, 1 + self.cnt)

    def test_recover(self):
        recover()
        chain_manager = blockchain.chain.ChainManager()
        self.assertEqual(chain_manager.main_chain.height, 1 + self.cnt)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    tests = [TestSaver('test_save'), TestSaver('test_recover')]
    suite.addTests(tests)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
