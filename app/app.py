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
STREAM_LENGTH = 10 #streamの長さ
SELL_BORDER = 70 #sell_pointと比べて売判断する閾値
BUY_BORDER = 70 #buy_pointと比べて買判断する閾値



#初期設定
data = {
    'stream': [],#データストリーム
    'status': 'idle',#sell,idleで保持状態を表記
    'sell_point': 0,
    'buy_point': 0,
}


while True:
    #データを取得（後にyfinanceで取得）
    now_price = func.dummy_price01()
    
    #データを格納
    data['stream'].append(now_price)

    if len(data['stream']) < STREAM_LENGTH:
        print('データ準備中')
    #データリストが特定以上になったら古い順に削除。
    else:
        data['stream'].pop(0)

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
    print(f"リスト:{data['stream']},sell:{data['sell_point']},buy:{data['buy_point']},status:{data['status']}")
    time.sleep(0.5)
