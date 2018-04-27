# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import ecdsa


def verify(pk, sig, msg):
    vkey = ecdsa.VerifyingKey.from_string(pk, curve=ecdsa.SECP256k1)
    vkey.verify(sig, msg)
