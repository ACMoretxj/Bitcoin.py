# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import hashlib


def sha(s):
    if not isinstance(s, bytes):
        s = s.encode()
    return hashlib.sha256(hashlib.sha256(s).digest()).hexdigest()
