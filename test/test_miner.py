# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
from unittest import TestCase

import blockchain.chain
import miner.miner


class TestMiner(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_mine(self):
        chain_manager = blockchain.chain.ChainManager()
        cnt = 10
        for i in range(cnt):
            block = miner.miner.Miner.mine()
            self.assertNotEqual(block, None)
            chain_manager.connect_block(block)
        self.assertEqual(chain_manager.main_chain.height, cnt + 1)
        blocks = chain_manager.main_chain.blocks
        for i, block in enumerate(blocks[:-1]):
            self.assertEqual(block.id, blocks[i + 1].prev_hash)


if __name__ == '__main__':
    unittest.main()
