# -*- coding: utf-8 -*-


def _safe_do(func, *args):
    try:
            return func(*args)
    except:
            return None
