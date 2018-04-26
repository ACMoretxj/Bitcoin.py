# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from uuid import uuid4

from blockchain.block import Block


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
