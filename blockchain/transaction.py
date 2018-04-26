# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import binascii
from collections import OrderedDict, namedtuple

from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5


class Transaction:

    TxIn = namedtuple('TxIn', [])

    def __init__(self, sender, passwd, receiver, value):
        """
        initialize the transaction
        :param sender: sender address
        :param passwd: sender private key
        :param receiver: receiver address
        :param value: send value
        """
        self.sender = sender
        self.passwd = passwd
        self.receiver = receiver
        self.value = value

    def sign(self):
        """
        sign the transaction using PKCS
        :return: the signature result
        """
        priv_key = RSA.importKey(binascii.unhexlify(self.passwd))
        signer = PKCS1_v1_5.new(priv_key)
        hsh = SHA.new(repr(self).encode('utf-8'))
        return binascii.hexlify(signer.sign(hsh)).decode('ascii')

    def verify(self, signature):
        """
        verify the transaction
        :param signature: signature of transaction to be verified
        :return: whether the transaction is valid or not
        """
        publ_key = RSA.importKey(binascii.unhexlify(self.sender))
        verifier = PKCS1_v1_5.new(publ_key)
        hsh = SHA.new(repr(self).encode('utf-8'))
        return verifier.verify(hsh, binascii.unhexlify(signature))

    def __repr__(self):
        data = OrderedDict({
            'sender': self.sender,
            'receiver': self.receiver,
            'value': self.value
        })
        return str(data)


class TransactionManager:

    MINING_SENDER = 'mining sender'

    def __init__(self):
        """
        initialize the transaction manager
        """
        self.transactions = []

    def submit(self, transaction, signature):
        """
        submit a transaction
        :param transaction: transaction to be submitted
        :param signature: the signature of transaction
        :return: success or not
        """
        # if the transaction is submitted by a miner,
        # just return true and reward it.
        if transaction.sender == self.MINING_SENDER:
            self.transactions.append(transaction)
            return True
        # the transaction occurs from one wallet to
        # another
        if transaction.verify(signature):
            self.transactions.append(transaction)
            return True
        return False
