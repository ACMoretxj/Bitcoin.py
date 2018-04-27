# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from functools import wraps

from copy import deepcopy


def singleton(cls):
    instances = {}

    @wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance


def copy_args(func):
    @wraps(func)
    def inner(*args, **kwargs):
        args = deepcopy(args)
        kwargs = deepcopy(kwargs)
        return func(args, kwargs)
    return inner
