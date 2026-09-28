import function as func
import random
import time

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
STREAM_LENGTH = 15 #streamの長さ
MA_SHORT_WIDTH = 5 #短期移動平均線計算時に使うデータのリスト幅
MA_LONG_WIDTH = 10 #長期移動平均線計算時に使うデータのリスト幅
BB_WIDTH = 10 #ボリンジャーバンド計算時に使うデータのリスト幅

SELL_BORDER = 70 #sell_pointと比べて売判断する閾値
BUY_BORDER = 70 #buy_pointと比べて買判断する閾値



#初期設定
data = {
    'stream': [],#データストリーム
    'status': 'idle',#sell,idleで保持状態を表記
    'sell_point': 0,
    'buy_point': 0,
    'ma_short_list': [],#短期移動平均線のリスト
    'ma_long_list': [],#長期移動平均線のリスト
    'bb_dict': {#ボリンジャーバンドの辞書型
        'up1': [],
        'down1': [],
        'up2': [],
        'down2': [],
    }
}


while True:
    #データを取得（後にyfinanceで取得）
    now_price = func.dummy_price01()
    
    #データを格納
    data['stream'].append(now_price)

    if len(data['stream']) <= STREAM_LENGTH:
        print('データ準備中')
        data['ma_short_list'].append(0)
        data['ma_long_list'].append(0)

        data['bb_dict']['up1'].append(0)#ここもっと簡略化できそう。
        data['bb_dict']['down1'].append(0)
        data['bb_dict']['up2'].append(0)
        data['bb_dict']['down2'].append(0)

    #データリストが特定以上になったら古い順に削除。
    else:
        #古いデータを削除（絶対最初に）
        data['stream'].pop(0)
        data['ma_short_list'].pop(0)
        data['ma_long_list'].pop(0)
        data['bb_dict']['up1'].pop(0)
        data['bb_dict']['down1'].pop(0)
        data['bb_dict']['up2'].pop(0)
        data['bb_dict']['down2'].pop(0)

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


        #売買点を計算（今はまだ）
        data['sell_point'] = random.randint(0,100)
        data['buy_point'] = random.randint(0,100)

        #売買判断を閾値で判定→取引→フラッグ
        if data['status']=='idle' and data['sell_point'] > SELL_BORDER:
            print('売り注文。')
            data['status'] = 'sell'
        elif data['status']=='sell' and data['buy_point'] < BUY_BORDER:
            print('取引完了。')
            data['status'] = 'idle'
    
    #ログに保存
    #print(f"リスト:{data['stream']},sell:{data['sell_point']},buy:{data['buy_point']},status:{data['status']}")
    print(data)
    time.sleep(0.5)
