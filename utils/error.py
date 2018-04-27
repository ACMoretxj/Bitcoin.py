# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from blockchain.block import Block
from blockchain.transaction import Transaction


class BaseError(BaseException):

    def __init__(self, msg):
        self.msg = msg


class TxValidationError(BaseError):

    def __init__(self, *args, to_orphan: Transaction=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.to_orphan = to_orphan


class BlockValidationError(BaseError):

    def __init__(self, *args, to_orphan: Block=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.to_orphan = to_orphan


class TxUnlockError(BaseError):
    pass
