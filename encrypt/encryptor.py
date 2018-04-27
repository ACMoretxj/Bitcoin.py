# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import hashlib
from base58 import b58encode_check


def pubkey_to_address(pubkey):
    if 'ripemd160' not in hashlib.algorithms_available:
        raise RuntimeError('missing ripemd160 hash algorithm')
    sha = hashlib.sha256(pubkey).digest()
    ripe = hashlib.new('ripemd160', sha).digest()
    return b58encode_check(b'\x00' + ripe)
