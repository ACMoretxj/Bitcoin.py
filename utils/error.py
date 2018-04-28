# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import blockchain.block
import blockchain.transaction


class BaseError(BaseException):

    def __init__(self, msg):
        self.msg = msg


class TxValidationError(BaseError):

    def __init__(self, *args, to_orphan=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.to_orphan = to_orphan


class BlockValidationError(BaseError):

    def __init__(self, *args, to_orphan=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.to_orphan = to_orphan


class TxUnlockError(BaseError):
    pass
