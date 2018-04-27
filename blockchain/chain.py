# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from uuid import uuid4

from blockchain.block import Block
from blockchain.settings import *
from utils import singleton


class Chain:

    def __init__(self):
        self.blocks = []

    @property
    def id(self):
        return str(uuid4()).replace('-', '')

    @property
    def height(self):
        return len(self.blocks)

    def locate(self, block_hash: str) -> (int, Block):
        for height, block in enumerate(self.blocks):
            if block.id == block_hash:
                return height, block
        return -1, None


@singleton
class ChainManager:

    def __init__(self):
        self.chains = []
        self.orphan_blocks = []
        self.main_chain_idx = None

    @property
    def main_chain(self):
        return self.chains[self.main_chain_idx]

    @property
    def block_subsidy(self):
        half_ratio = len(self.main_chain) // HALF_SUBSIDY_AFTER_BLOCK_NUM
        if half_ratio > MAX_HALF_RATIO: return 0
        return INITIAL_COIN_SUBSIDY * MONEY_PER_COIN // 2 ** half_ratio

    def locate_block(self, block_hash, chain=None) -> (Block, int, str):
        _chains = {chain.id: chain} if chain else self.chains
        for chain_id, _chain in _chains.items():
            height, block = _chain.locate(block_hash)
            if not block: continue
            return block, height, chain_id
        return None, -1, None
