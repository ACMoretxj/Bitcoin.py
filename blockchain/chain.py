# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from uuid import uuid4

import blockchain.block
import blockchain.transaction
import blockchain.mempool

import miner
import server.encoder
import server.peer
from encrypt import sha

from utils import singleton
import utils.error


class Chain:

    def __init__(self, blocks=None):
        self.blocks = blocks or []
        # key: transaction id, value: (transaction, height)
        self.inv_txns = {}

    @property
    def id(self):
        return str(uuid4()).replace('-', '')

    @property
    def height(self):
        return len(self.blocks)

    def add(self, block):
        self.blocks.append(block)
        for height, txn in enumerate(block.txn_manager.txns):
            self.inv_txns[txn.id] = txn, height

    def pop(self):
        block = self.blocks.pop()
        for txn in block.txn_manager.txns:
            del self.inv_txns[txn.id]
        return block

    def locate(self, block_hash):
        for height, block in enumerate(self.blocks):
            if block.id == block_hash:
                return height, block
        return -1, None


@singleton
class ChainManager:

    def __init__(self):
        genesis_block = blockchain.block.Block(
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
        self.chains = [Chain([genesis_block])]
        self.orphan_blocks = []
        self.main_chain_idx = 0

    @property
    def main_chain(self):
        return self.chains[self.main_chain_idx]

    @property
    def side_chains(self):
        return self.chains[1:]

    def organize_branch(self, branch, branch_idx, fork_idx):
        def disconnect_to_fork(_fork_block):
            while self.main_chain.blocks[-1].id != _fork_block.id:
                yield self.disconnect_block(self.main_chain.blocks[-1])

        def rollback(_fork_block, _old_blocks):
            list(disconnect_to_fork(_fork_block))
            # noinspection PyShadowingNames
            for block in _old_blocks:
                assert self.connect_block(block, doing_reorg=True)\
                       == self.main_chain_idx

        fork_block = self.main_chain.blocks[fork_idx]
        old_blocks = list(disconnect_to_fork(fork_block))[::-1]
        for block in branch.blocks:
            connected_idx = self.connect_block(block, doing_reorg=True)
            if connected_idx != self.main_chain_idx:
                rollback(fork_block, old_blocks)
                return False
        assert branch.blocks[0].prev_hash == self.main_chain.blocks[-1].id

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
            branch_height = len(branch.blocks) + fork_idx

            if branch_height > main_height:
                reorged |= self.organize_branch(branch, branch_idx, fork_idx)

        return reorged

    def locate_block(self, block_hash, chain=None):
        _chains = [chain] if chain else self.chains
        for chain_id, _chain in enumerate(_chains):
            height, block = _chain.locate(block_hash)
            if not block: continue
            return block, height, chain_id
        return None, -1, None

    def connect_block(self, block, doing_reorg=False):
        from .transaction import UTXOManager
        search_chain = self.main_chain if doing_reorg else None
        if self.locate_block(block.id, chain=search_chain)[0]:
            return None

        try: block, chain_idx = block.validate()
        except utils.error.BlockValidationError as e:
            if e.to_orphan:
                self.orphan_blocks.append(e.to_orphan)
            return None

        if chain_idx != self.main_chain_idx and len(self.chains) <= chain_idx:
            self.chains.append(Chain())
        chain = self.main_chain if chain_idx == self.main_chain_idx \
            else self.chains[chain_idx]
        chain.add(block)

        mempool = blockchain.mempool.Mempool()
        utxo_manager = UTXOManager()
        peer_manager = server.peer.PeerManager()

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
                    utxo_manager.add(txout, txn, i, txn.is_coinbase, len(chain.blocks))

        if (not doing_reorg and self.reorganize()) \
                or chain_idx == self.main_chain_idx:
            miner.mine_interrupt.set()

        peer_manager.notify_all_peers(server.encoder.encode_http_data(block))

        return chain_idx

    def disconnect_block(self, block, chain=None):
        from .transaction import UTXOManager
        mempool = blockchain.mempool.Mempool()
        utxo_manager = UTXOManager()

        chain = chain or self.main_chain
        assert block == chain.blocks[-1], 'The block being disconnected must' \
                                          ' be the tail of chain'
        for txn in block.txn_manager.txns:
            mempool.add_transaction(txn)
            for txin in txn.txins:
                if txin.txid:
                    # the txn is just in the block, the real txn which txin.idx
                    # points may be in other block
                    chain_txn, height = chain.inv_txns[txin.txid]
                    utxo_manager.add(chain_txn[txin.txout_idx],
                                     chain_txn, txin.idx,
                                     chain_txn.is_coinbase, height)
            for i, _ in enumerate(txn.txouts):
                utxo_manager.remove(txn.id, i)

        return chain.pop()
