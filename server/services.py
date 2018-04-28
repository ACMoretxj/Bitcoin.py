# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import threading

from flask import Flask, request, jsonify

import server.encoder
import server.peer
import blockchain.mempool
import blockchain.chain
import miner.miner
from utils import singleton

app = Flask(__name__)


@app.route('/put/transaction', methods=['POST'])
def put_transaction():
    data = request.values.get('data')
    txn = server.encoder.decode_http_data(data)
    mempool = blockchain.mempool.Mempool()
    mempool.add_transaction(txn)
    return jsonify({'status': 'ok'})


@app.route('/put/block', methods=['POST'])
def put_block():
    data = request.values.get('data')
    block = server.encoder.decode_http_data(data)
    chain_manager = blockchain.chain.ChainManager()
    chain_manager.connect_block(block)
    return jsonify({'status': 'ok'})


@app.route('/get/blocks', methods=['GET'])
def get_blocks():
    chain_manager = blockchain.chain.ChainManager()
    blocks = chain_manager.main_chain.blocks
    blocks = [server.encoder.encode_http_data(b) for b in blocks]
    return jsonify(blocks)


@singleton
class Service:

    def __init__(self):
        self.port = 8080
        self.servers = []

    def create_server(self):
        self.port += 1
        self.servers.append(threading.Thread(
            target=lambda port: app.run(host='localhost', port=port),
            args=(self.port,), daemon=False))
        self.servers[-1].start()


if __name__ == '__main__':
    service = Service()
    for i in range(1):
        service.create_server()
    # miner_thread = threading.Thread(
    #     target=lambda: miner.miner.Miner.mine_forever(), daemon=False
    # )
    # miner_thread.run()
