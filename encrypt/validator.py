# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import ecdsa


def verify(pk, sig, msg):
    vkey = ecdsa.VerifyingKey.from_string(pk, curve=ecdsa.SECP256k1)
    vkey.verify(sig, msg)


def new_signing_key():
    return ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)


def get_signing_key(s):
    ecdsa.SigningKey.from_string(s, curve=ecdsa.SECP256k1)


def get_verifying_key(signing_key):
    return signing_key.get_verifying_key()
