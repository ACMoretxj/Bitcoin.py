# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from blockchain.transaction import Transaction, TxIn, TxOut


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
        return TxIn(_txin['id'], _txin['txout_idx'],
                    _txin['unlock_sig'], _txin['unlock_pk'])

    def decode_txout(_txout):
        _txout = eval(_txout)
        return TxOut(_txout['value'], _txout['receiver'])

    txn = Transaction(txins=[decode_txin(txin) for txin in data['txins']],
                      txouts=[decode_txout(txout) for txout in data['txouts']])
    return txn


def encode_http_data(origin):
    if isinstance(origin, Transaction):
        return __encode_transaction(origin)
    else: return None


def decode_http_data(origin):
    origin = eval(origin)
    if origin['type'] == 'transaction':
        return __decode_transaction(origin)
    else: return None
