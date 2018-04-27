# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from uuid import uuid4

from blockchain import mempool, utxo_manager, peer_manager
from blockchain.block import Block
from blockchain.settings import *
from miner import mine_interrupt
from server import encode_http_data
from utils import singleton, BlockValidationError


class Chain:

    def __init__(self, blocks=None):
        self.blocks = blocks or []
        # key: transaction id, value: transaction
        self.inv_txns = {}

    @property
    def id(self):
        return str(uuid4()).replace('-', '')

    @property
    def height(self):
        return len(self.blocks)

    def add(self, block):
        self.blocks.append(block)
        for txn in block.txn_manager.txns:
            self.inv_txns[txn.id] = txn

    def pop(self):
        block = self.blocks.pop()
        for txn in block.txn_manager.txns:
            del self.inv_txns[txn.id]
        return block

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
        if self.main_chain_idx is None: return None
        return self.chains[self.main_chain_idx]

    @property
    def side_chains(self):
        return self.chains[1:]

    def organize_branch(self, branch, branch_idx, fork_idx):
        def disconnect_to_fork():
            while self.main_chain[-1].id != fork_block.id:
                yield self.disconnect_block(self.main_chain[-1])

        def rollback():
            list(disconnect_to_fork())
            # noinspection PyShadowingNames
            for block in old_blocks:
                assert self.connect_block(block, doing_reorg=True)\
                       == self.main_chain_idx

        for block in branch.blocks:
            connected_idx = self.connect_block(block, doing_reorg=True)
            if connected_idx != self.main_chain_idx:
                rollback()
                return False

        fork_block = self.main_chain[fork_idx]
        old_blocks = list(disconnect_to_fork())[::-1]
        assert branch.blocks[0].prev_hash == self.main_chain[-1].id

        self.chains.pop(branch_idx - 1)
        self.chains.append(Chain(old_blocks))

        return True

    def reorganize(self):
        reorged = False
        frozen_side_branches = list(self.side_chains)

        for branch_idx, branch in enumerate(frozen_side_branches, 1):
            fork_block, fork_idx, _ = self.locate_block(
                branch.blocks[0].prev_hash, self.main_chain)
            main_height = self.main_chain.height
            branch_height = len(branch) + fork_idx

            if branch_height > main_height:
                reorged |= self.organize_branch(branch, branch_idx, fork_idx)

        return reorged

    def locate_block(self, block_hash, chain=None) -> (Block, int, str):
        _chains = {chain.id: chain} if chain else self.chains
        for chain_id, _chain in _chains.items():
            height, block = _chain.locate(block_hash)
            if not block: continue
            return block, height, chain_id
        return None, -1, None

    def connect_block(self, block, doing_reorg):
        search_chain = self.main_chain if doing_reorg else None
        if self.locate_block(block.id, chain=search_chain)[0]:
            return None

        try: block, chain_idx = block.validate()
        except BlockValidationError as e:
            if e.to_orphan:
                self.orphan_blocks.append(e.to_orphan)
            return None

        if chain_idx != self.main_chain_idx and len(self.chains) <= chain_idx:
            self.chains.append(Chain())
        chain = self.main_chain if chain_idx == self.main_chain_idx \
            else self.chains[chain_idx]
        chain.add(block)

        if chain_idx == self.main_chain_idx:
            for txn in block.txn_manager.txns:
                mempool.del_transaction(txn.id)
                # now the block is in use, so really spend the money
                # it plans to (actually just remove the utxo)
                if not txn.is_coinbase:
                    for txin in txn.txins:
                        utxo_manager.remove(txn.id, txin.txout_idx)
                # Alice's spend means Bob's gain, so add new utxo
                for i, txout in enumerate(txn.txouts):
                    utxo_manager.add(txout, txn, i, txn.is_coinbase, len(chain))

        if (not doing_reorg and self.reorgnize()) \
                or chain_idx == self.main_chain_idx:
            mine_interrupt.set()

        peer_manager.notify_all_peers(encode_http_data(block))

        return chain_idx

    def disconnect_block(self, block, chain=None):
        chain = chain or self.main_chain
        assert block == chain[-1], 'The block being disconnected must ' \
                                   'be the tail of chain'
        for txn in block.txn_manager.txns:
            mempool.add_transaction(txn)
            for txin in txn.txins:
                if txin.idx:
                    utxo_manager.add(chain.inv_txns[txin.idx][txin.txout_idx])
            for i, _ in enumerate(txn.txouts):
                utxo_manager.remove(txn.id, i)

        return chain.pop()
