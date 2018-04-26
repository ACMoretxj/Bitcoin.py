# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from blockchain.block import Block
from blockchain.chain import Chain

main_chain_id = None
chains = {}
orphan_blocks = []
utxos = {}


def locate_block(block_hash: str, chain: Chain=None) -> (Block, int, str):
    global chains

    _chains = {chain.id: chain} if chain else chains
    for chain_id, _chain in _chains.items():
        height, block = _chain.locate(block_hash)
        if not block: continue
        return block, height, chain_id
    return None, -1, None
