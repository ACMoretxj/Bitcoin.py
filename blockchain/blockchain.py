# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from blockchain.chain import ChainManager
from blockchain.mempool import Mempool
from blockchain.transaction import UTXOManager

chain_manager = ChainManager()
utxo_manager = UTXOManager()
mempool = Mempool()


if __name__ == '__main__':
    pass
