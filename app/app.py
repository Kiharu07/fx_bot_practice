import function as func
import random
import time
import yfinance as yf
import pandas as pd

#大挙動
"""
初期設定
データをリストに格納
閾値を計算
取引
ログに保存
"""

#小挙動
"""
初期設定
データを格納
データリストが特定以上になったら古い順に削除。
閾値を計算
取引→フラッグ
ログに保存
"""

#定数置き場：開発途中でconfig.yamlに移します。
INTERVAL = 2 #データ取得間隔（秒） 
STREAM_LENGTH = 15 #streamの長さ
MA_SHORT_WIDTH = 5 #短期移動平均線計算時に使うデータのリスト幅
MA_LONG_WIDTH = 10 #長期移動平均線計算時に使うデータのリスト幅
BB_WIDTH = 10 #ボリンジャーバンド計算時に使うデータのリスト幅

SELL_BORDER = 9 #sell_pointと比べて売判断する閾値
SELL_STOP_BORDER = 70 #sell_stop_pointと比べて取引終了判断する閾値

GOLDEN_CROSS = 1 #ゴールデンクロスのフラッグ
DEAD_CROSS = -1 #デッドクロスのフラッグ

#ストラテジー重み格納庫：こちらも開発途中でconfig.yamlに移します。
WEIGHT_MA_LONG_OVER_SHORT = 10 #長期移動平均線が短期移動平均線を上回っているかどうかの重み

if __name__ == "__main__":
    print('app.pyを実行します。')

#初期設定
data = {
    'trade_price': 0,#取引価格
    'stream': {
         'close': [],
         'high': [],
         'low': [],
         'open': [],
         'volume': [],
    },#データストリーム
    'status': 'idle',#sell,idleで保持状態を表記
    'sell_point': 0,
    'sell_stop_point': 0,
    'ma_short_list': [],#短期移動平均線のリスト
    'ma_long_list': [],#長期移動平均線のリスト
    'bb_dict': {#ボリンジャーバンドの辞書型
        'up1': [],
        'down1': [],
        'up2': [],
        'down2': [],
    },
    "cross_list": [],#ゴールデン、デッドクロスのリスト
}


while True:
    information_set = yf.download("JPY=X", period="1d", interval="1m") #期間1日で1分足のデータを取得(テストなので。のちに５分足や15分足に変更予定)
    latest = information_set.iloc[-1] #最新のデータを取得

    now_close = latest['Close']['JPY=X'] #最新の終値を取得
    now_high = latest['High']['JPY=X'] #最新の最高値を取得
    now_low = latest['Low']['JPY=X'] #最新の最低値を取得
    now_open = latest['Open']['JPY=X'] #最新の始値を取得
    now_volume = latest['Volume']['JPY=X'] #最新の出来高を取得

    #データを取得（後にyfinanceで取得）
    
    #データを格納
    data['stream']['close'].append(now_close)
    data['stream']['high'].append(now_high)
    data['stream']['low'].append(now_low)
    data['stream']['open'].append(now_open)
    data['stream']['volume'].append(now_volume)

    if len(data['stream']['close']) <= STREAM_LENGTH:
        print('データ準備中')
        data['ma_short_list'].append(0)
        data['ma_long_list'].append(0)

        data['bb_dict']['up1'].append(0)#ここもっと簡略化できそう。
        data['bb_dict']['down1'].append(0)
        data['bb_dict']['up2'].append(0)
        data['bb_dict']['down2'].append(0)

        data['cross_list'].append(0)

    #データリストが特定以上になったら古い順に削除。
    else:
        #古いデータを削除（絶対最初に）
        data['stream']['close'].pop(0)
        data['stream']['high'].pop(0)
        data['stream']['low'].pop(0)
        data['stream']['open'].pop(0)
        data['stream']['volume'].pop(0)     
        data['ma_short_list'].pop(0)
        data['ma_long_list'].pop(0)
        data['bb_dict']['up1'].pop(0)
        data['bb_dict']['down1'].pop(0)
        data['bb_dict']['up2'].pop(0)
        data['bb_dict']['down2'].pop(0)
        data['cross_list'].pop(0)

        #テクニカル指標の格納
        ma_short = func.ma(data,STREAM_LENGTH-MA_SHORT_WIDTH,STREAM_LENGTH)#短期ma
        data['ma_short_list'].append(ma_short)

        ma_long = func.ma(data,STREAM_LENGTH-MA_LONG_WIDTH,STREAM_LENGTH)#長期ma
        data['ma_long_list'].append(ma_long)

        bb_set = func.bb(data,STREAM_LENGTH-BB_WIDTH,STREAM_LENGTH)#bb_set = [up1,down1,up2,down2]
        data['bb_dict']['up1'].append(bb_set[0])
        data['bb_dict']['down1'].append(bb_set[1])
        data['bb_dict']['up2'].append(bb_set[2])
        data['bb_dict']['down2'].append(bb_set[3])

        #ゴールデンクロス、デッドクロスの判定、格納。
        if func.is_golden_cross(data):
                data['cross_list'].append(GOLDEN_CROSS)
        elif func.is_dead_cross(data):
                data['cross_list'].append(DEAD_CROSS)
        else:
                data['cross_list'].append(0)

        """↑テクニカル指標操作ここまで↑（↓ここから下は判定↓）"""

        #戦略ブロック算定
        sell_1 = func.st_ma_long_over_short(data)*WEIGHT_MA_LONG_OVER_SHORT

        s_stop_1 = func.st_ma_long_over_short(data)*WEIGHT_MA_LONG_OVER_SHORT

        
        #売買点を計算（今はまだ）
        data['sell_point'] = sell_1 #今後ここに足していく
        data['sell_stop_point'] = random.randint(0,100)#上と同じようにs_stop_1を足していく


        #売買判断を閾値で判定→取引→フラッグ
        if data['status']=='idle' and data['sell_point'] >= SELL_BORDER:
            print('売り注文。')
            data['status'] = 'sell'
            data['trade_price'] = now_close
        elif data['status']=='sell' and data['sell_stop_point'] <= SELL_STOP_BORDER:
            print('取引完了。')
            data['status'] = 'idle'
            data['trade_price'] = 0 #ここでバグが発生するかも。
    #ログに保存
    #print(f"リスト:{data['stream']},sell:{data['sell_point']},buy:{data['sell_stop_point']},status:{data['status']}")
    print(data)
    time.sleep(INTERVAL)