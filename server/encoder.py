# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import blockchain.block
import blockchain.transaction


def __encode_transaction(txn):
    def encode_txin(_txin):
        return {
            'txid': _txin.txid,
            'txout_idx': _txin.txout_idx,
            'unlock_sig': _txin.unlock_sig,
            'unlock_pk': _txin.unlock_pk
        }

    def encode_txout(_txout):
        return {
            'value': _txout.value,
            'receiver': _txout.receiver
        }

    data = {
        'type': 'transaction',
        'txins': [encode_txin(txin) for txin in txn.txins],
        'txouts': [encode_txout(txout) for txout in txn.txouts]
    }
    return data


def __decode_transaction(data):
    def decode_txin(_txin):
        _txin = eval(_txin)
        return blockchain.transaction.TxIn(_txin['id'], _txin['txout_idx'],
                                _txin['unlock_sig'], _txin['unlock_pk'])

    def decode_txout(_txout):
        _txout = eval(_txout)
        return blockchain.transaction.TxOut(_txout['value'], _txout['receiver'])

    txn = blockchain.transaction.Transaction(txins=[decode_txin(txin) for txin in data['txins']],
                                  txouts=[decode_txout(txout) for txout in data['txouts']])
    return txn


def __encode_block(block):
    data = {
        'version': block.version,
        'prev_hash': block.prev_hash,
        'merkle_hash': block.merkle_hash,
        'bits': block.bits,
        'nonce': block.nonce,
        'transactions': [__encode_transaction(txn)
                         for txn in block.txn_manager.txns],
        'stamp': block.stamp
    }
    return data


def __decode_block(data):
    txn_manager = blockchain.transaction.TransactionManager(__decode_block(txn)
                                     for txn in data['transactions'])
    block = blockchain.block.Block(version=int(data['version']), prev_hash=data['prev_hash'],
                                   merkle_hash=data['merkle_hash'], bits=data['bits'],
                                   nonce=data['nonce'], txn_manager=txn_manager,
                                   stamp=int(data['stamp']))
    return block


def encode_http_data(origin):
    if isinstance(origin, blockchain.transaction.Transaction):
        return __encode_transaction(origin)
    if isinstance(origin, blockchain.block.Block):
        return __encode_block(origin)
    else: return None


def decode_http_data(data):
    data = eval(data)
    if data['type'] == 'transaction':
        return __decode_transaction(data)
    if data['type'] == 'block':
        return __decode_block(data)
    else: return None
