import random

"""ダミーデータ（開発用）"""
def dummy_price01()->float:
    """
    dummy_の値段をfloatで返す。
    完全な乱数なので傾向などは無い。
    """
    amplitude = 0.1*random.randint[-100,100]#変化幅(-10<x<10)
    val = 140 + amplitude 
    return val

"""売買点関係"""