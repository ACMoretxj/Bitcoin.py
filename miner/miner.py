# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from time import time

from blockchain import chain_manager
from blockchain.block import Block
from blockchain.wallet import init_wallet
from encrypt import sha
from miner import mine_interrupt


class Miner:

    def __init__(self):
        pass

    @staticmethod
    def mine():
        my_address = init_wallet()[2]
        block = Block.new_block(my_address)

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
        while True:
            block = Miner.mine()
            if block: chain_manager.connect_block(block)
