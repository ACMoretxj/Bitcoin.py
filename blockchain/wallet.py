# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import functools

import os

from .settings import DEFAULT_WALLET_PATH
from encrypt import get_signing_key, new_signing_key, get_verifying_key, \
    pubkey_to_address


@functools.lru_cache()
def init_wallet(path=None):
    path = path or DEFAULT_WALLET_PATH

    if os.path.exists(path):
        with open(path, 'rb') as f:
            signing_key = get_signing_key(f.read())
    else:
        signing_key = new_signing_key()
        with open(path, 'wb') as f:
            f.write(signing_key.to_string())

    verifying_key = get_verifying_key(signing_key)
    my_address = pubkey_to_address(verifying_key.to_string())

    return signing_key, verifying_key, my_address
