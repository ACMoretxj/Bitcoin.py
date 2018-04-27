# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from .transaction import UTXOManager
from .chain import ChainManager
from .mempool import Mempool
from server.peer import PeerManager

utxo_manager = UTXOManager()
chain_manager = ChainManager()
mempool = Mempool()
peer_manager = PeerManager()
