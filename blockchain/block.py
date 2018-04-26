# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import hashlib
from collections import namedtuple
from time import time

from blockchain.error import BlockValidationError
from blockchain.settings import *


class Block:

    BlockHeader = namedtuple('BlockHeader',
                             ['version', 'prev_hash', 'merkle_hash', 'bits',
                              'nonce', 'stamp'])

    def __init__(self, version, prev_hash, merkle_hash, bits, nonce,
                 trans_manager, stamp=time()):
        self.version = version
        self.prev_hash = prev_hash
        self.merkle_hash = merkle_hash
        self.bits = bits
        self.nonce = nonce
        self.trans_manager = trans_manager
        self.stamp = stamp

    @property
    def header(self):
        return self.BlockHeader(self.version, self.prev_hash, self.merkle_hash,
                                self.bits, self.nonce, self.stamp)

    @property
    def id(self):
        return hash(self)

    @property
    def next_bits(self):
        if not self.prev_hash:
            return INITIAL_DIFFICULTY
        # TODO

    @property
    def fees(self):
        fee = 0

        return fee

    def validate(self):
        if not self.trans_manager:
            raise BlockValidationError('Transactions are empty')
        if int(self.id) > (1 << (256 - self.bits)):
            raise BlockValidationError('Block header doesn\'t satisfy bits')

    def __repr__(self):
        return str(self.header)

    def __hash__(self):
        return hashlib.sha256(self).hexdigest()
