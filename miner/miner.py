# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import threading
from time import time

import blockchain.block
import blockchain.wallet
import blockchain.chain
from encrypt import sha


mine_interrupt = threading.Event()


class Miner:

    def __init__(self):
        pass

    @staticmethod
    def mine(prev_hash=None):
        block = blockchain.block.Block.new_block(prev_hash)
        nonce, target = 0, 1 << (256 - block.bits)
        mine_interrupt.clear()

        while True:
            block.nonce = nonce
            if int(sha(block.header), 16) < target:
                break
            nonce += 1
            if nonce % 10000 == 0 and mine_interrupt.is_set():
                mine_interrupt.clear()
                return None
        return block

    @staticmethod
    def mine_forever():
        chain_manager = blockchain.chain.ChainManager()
        while True:
            block = Miner.mine()
            if block: chain_manager.connect_block(block)
#
#
# if __name__ == '__main__':
#     cm = blockchain.chain.ChainManager()
#     for i in range(1000):
#         blk = Miner.mine()
#         cm.connect_block(blk)
#         print('current index: %d, difficulty: %d, hash: %s' % (i, blk.bits, blk.id))
