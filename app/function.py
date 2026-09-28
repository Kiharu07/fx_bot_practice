import random

#定数置き場：開発途中でconfig.yamlに移します。
STREAM_LENGTH = 15 #streamの長さ
MA_SHORT_WIDTH = 5 #短期移動平均線計算時に使うデータのリスト幅
MA_LONG_WIDTH = 10 #長期移動平均線計算時に使うデータのリスト幅
BB_WIDTH = 10 #ボリンジャーバンド計算時に使うデータのリスト幅

SELL_BORDER = 70 #sell_pointと比べて売判断する閾値
BUY_BORDER = 70 #buy_pointと比べて買判断する閾値

"""オートメーション"""


"""ダミーデータ（開発用）"""
def dummy_price01()->float:
    """
    dummy_の値段をfloatで返す。\n
    完全な乱数なので傾向などは無い。
    """
    amplitude = 0.1*random.randint(-100,100)#変化幅(-10<x<10)
    val = 140 + amplitude 
    return val

"""テクニカル指標関係"""
def ma(data:dict,start_index:int,end_index:int)->float:
    """
    移動平均線を計算する。\n
    start_indexからend_indexまでの平均値を返す。
    """
    sum = 0
    for i in range(start_index,end_index):
        sum += data['stream'][i]
    ave = sum / (end_index - start_index)
    return ave

def bb(data:dict,start_index:int,end_index:int)->list:
    """
    リストで[up1,down1,up2,down2]を返す。\n
    start_indexからend_indexまでの標準偏差を返す。
    """
    ave = ma(data,start_index,end_index)
    sum = 0
    for i in range(start_index,end_index):
        sum += (data['stream'][i] - ave)**2
    std = (sum / (end_index - start_index))**0.5
    up1 = ave + std
    down1 = ave - std
    up2 = ave + 2*std
    down2 = ave - 2*std
    return [up1,down1,up2,down2]

def is_golden_cross(data:dict)->bool:
    """
    ゴールデンクロスかどうかを判定する。\n
    直近の2データの短期移動平均線が長期移動平均線を下から上に突き抜けたらTrueを返す。
    """
    if data['ma_short_list'][-2] < data['ma_long_list'][-2] and data['ma_short_list'][-1] > data['ma_long_list'][-1]:
        return True
    else:
        return False