import okx.Account as Account
import okx.Trade as Trade
import okx.MarketData as MarketData
import pandas as pd
import datetime
import logging
import json
import time
import finta
import configparser
import random

# 配置文件读取API初始化信息
config = configparser.ConfigParser()
config.read('config.ini')

apikey = config['OKX']['apikey']
secretkey = config['OKX']['secretkey']
passphrase = config['OKX']['passphrase']
flag = config['OKX']['flag']  # 实盘:0 , 模拟盘:1

accountAPI = Account.AccountAPI(apikey, secretkey, passphrase, False, flag)
tradeAPI = Trade.TradeAPI(apikey, secretkey, passphrase, False, flag)
marketDataAPI = MarketData.MarketAPI(flag=flag)
bz = "BTC-USDT-SWAP"
dbz = "BTC"

def setGgbnum():
    # 在逐仓交易模式下，设置币币杠杆的杠杆倍数（币对层面）
    result = accountAPI.set_leverage(
        instId=bz,
        lever="20",
        mgnMode="cross"
    )
    print(result)
    return result

# 其他辅助函数...
def getOrder(oid):
    result = tradeAPI.get_order(
        instId=bz,
        # ordId=oid,
        clOrdId=oid
    )
    print(result)
 
    return result


def generate_order_id():
    # 生成一个新的随机订单号
    return random.randint(10000, 99999)


def tradedata():
    result = tradeAPI.get_orders_history(
        instType="SPOT",
        ordType="market,post_only,fok,ioc"
    )
  
    return result

'''
产品类型
SPOT：币币
SWAP：永续合约
'''
def  getTicker():
# 获取所有产品行情信息

    result = marketDataAPI.get_tickers(
    instType="SWAP"
    )
    return result 


def positions():
    result = accountAPI.get_positions(
        instType="SWAP",
        instId=bz
    )
   
    return result


# 配置日志
logging.basicConfig(filename='trading_btc.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',encoding='utf-8')

def log_dictionary(dict_data):
    """
    记录字典内容到日志文件中，确保中文字符可读
    """
    try:
        # 将字典转换为 JSON 字符串，并确保中文字符被正确解码
        dict_as_string = json.dumps(dict_data, indent=4, ensure_ascii=False)
        # 将字符串写入日志
        logging.info(dict_as_string)
    except Exception as e:
        logging.error(f"Error logging dictionary: {e}")


def account(cb):
    for attempt in range(3):  # 尝试次数
        try:
            result = accountAPI.get_account_balance(
                ccy=cb
            )
            
            return result["data"][0]
        except Exception as e:
            print(f"Error: {e}")
            if attempt < 2:  # 如果这不是最后一次尝试，等待2秒然后再次尝试
                time.sleep(2)
            else:
                print("Failed to get account balance after 3 attempts.")
                return None  # 或者返回一个错误值/异常，让调用者知道请求失败

def jy():
    global position_opened
    global order_id

    # 获取历史数据
    # small_period = "5m"  # 可以根据需要修改,如 "5m"、"15m"、"1h" 等
    historical_data = marketDataAPI.get_candlesticks(instId=bz, bar="5m", limit="155")
  
    data1 = pd.DataFrame(historical_data["data"], columns=["ts", "open", "high", "low", "close", "vol", "volCcy", "volCcyQuote", "confirm"])
    # data1['ts'] = data1['ts'].apply(lambda x: datetime.datetime.fromtimestamp(int(x) / 1000))
    # data1['ts'] = data1['ts'].dt.strftime('%Y-%m-%d %H:%M:%S')
    # data1.set_index('ts', inplace=True)

    # large_period = "30m"  # 可以根据需要修改,如 "30m"、"1h"、"2h" "4h"等
    historical_data1 = marketDataAPI.get_candlesticks(instId=bz, bar="30m", limit="70")
 
    data2 = pd.DataFrame(historical_data1["data"], columns=["ts", "open", "high", "low", "close", "vol", "volCcy", "volCcyQuote", "confirm"])
    data2['ts'] = data2['ts'].apply(lambda x: datetime.datetime.fromtimestamp(int(x) / 1000))
    data2['ts'] = data2['ts'].dt.strftime('%Y-%m-%d %H:%M:%S')
    data2.set_index('ts', inplace=True)
    # print(data1['close'])
    # print(data1)
    # print(data2['close'])
    # exit(1)

    
    # 计算EMA值
    ma_small = finta.TA.EMA(data1, 10)
    ma1_small = finta.TA.EMA(data1, 150)
    # print(ma_small)
    # print(ma1_small.iloc[148])
    # ma_large = finta.TA.SMA(data2, 60)

    macd1 = finta.TA.MACD(data1,15,34)
    macd2 = finta.TA.MACD(data2,15,34)
    
    # print(macd1)
    # a = getTicker()['data']
    # for n in a:
    #     num = float(n['volCcy24h']) * float(n['last']) / 100000000
    #     if num > 2 and "USDT" in n['instId']:
    #         print(n['instId'],"---",round(num,2),"亿")
    a = getTicker()['data']
# 创建一个列表，存储交易对的ID和计算出的交易量
    trades = [(n['instId'], float(n['volCcy24h']) * float(n['last']) / 100000000) for n in a if "USDT" in n['instId'] \
              and float(n['volCcy24h']) * float(n['last']) / 100000000 > 5 and float(n['last']) > 0 ]

# 根据交易量对列表进行排序，降序排列
    sorted_trades = sorted(trades, key=lambda x: x[1], reverse=True)

# 打印排序后的交易对和交易量
    for instId, num in sorted_trades:
        print(instId, "---", round(num, 2), "亿")
    exit(1)
    ma150_small = finta.TA.SMA(data1, 150)
    ma120_small = finta.TA.SMA(data1, 120)
    ma120_large = finta.TA.SMA(data2, 120)
    ma150_large = finta.TA.SMA(data2, 150)

    # # 添加止盈止损
    # take_profit = 0.025  # 止盈比例,可调整
    # stop_loss = 0.025  # 止损比例,可调整

    # EMA顺势指标开仓条件
    if position_opened == False:
        print('start diff')
        # print(ma_large.iloc[59])
        # # print(ma_small)
        # exit(110)
        # if float(data1['close'].iloc[1]) > float(ma_large.iloc[238]) and float(data1['close'].iloc[0]) < float(ma_small.iloc[9]):  # 下穿MA10开空
        # if float(ma_small.iloc[8]) < float(ma_large.iloc[58]) and float(ma_small.iloc[9]) < float(ma_large.iloc[59]) and float(data1['close'].iloc[1]) > float(ma_small.iloc[8]) and float(data1['close'].iloc[0]) < float(ma_small.iloc[9]):  # 下穿MA10开空
        if float(ma_small.iloc[8]) < float(ma_large.iloc[58]) \
        and float(ma_small.iloc[9]) < float(ma_large.iloc[59]) \
        and float(data1['close'].iloc[1]) > float(ma_small.iloc[8]) \
        and float(data1['close'].iloc[0]) < float(ma_small.iloc[9]):  # 下穿MA10开空
            order_id = generate_order_id()
            print('echo 1111')
            open_position("sell")
        # if float(data1['close'].iloc[1]) > float(ma_large.iloc[238]) and float(data1['close'].iloc[0]) < float(ma_small.iloc[9]):  # 下穿MA10开空
        # elif float(ma_small.iloc[8]) > float(ma_large.iloc[58]) and float(ma_small.iloc[9]) > float(ma_large.iloc[59]) and float(data1['close'].iloc[1]) < float(ma_small.iloc[8]) and float(data1['close'].iloc[0]) > float(ma_small.iloc[9]):  # 上穿MA10开多
        elif float(ma_small.iloc[8]) > float(ma_large.iloc[58]) \
        and float(ma_small.iloc[9]) > float(ma_large.iloc[59]) \
        and float(data1['close'].iloc[1]) < float(ma_small.iloc[8]) \
        and float(data1['close'].iloc[0]) > float(ma_small.iloc[9]):  # 上穿MA10开多
            order_id = generate_order_id()     
            open_position("buy")

    # 持仓中止盈止损
    elif position_opened:
        print("zhi y zhi s")
        pos_data = positions()['data'][0]
        print(pos_data)
        # cur_price = float(data1['close'].iloc[-1])
        # entry_price = float(pos_data['avgPx'])  # 持仓均价
        pnl = float(pos_data['upl'])  # 浮动盈亏
        pnlrao = float(pos_data['uplRatio'])  # 浮动盈亏%
        # print(type(pnl),pnl)
        # print(type(entry_price),entry_price)

        # if pnl > 0 and (cur_price - entry_price) / entry_price >= take_profit:  # 止盈
        #     close_position(pos_data['posSide'])
        # elif pnl < 0 and (entry_price - cur_price) / entry_price >= stop_loss:  # 止损  
        #     close_position(pos_data['posSide'])
        if pnl > 50 or pnlrao < -0.1:  # 平仓 ,亏损或盈利达预期则平仓
        # if abs(pnl) >= 1:  # 平仓 ,亏损或盈利达预期则平仓
        # if  pnlrao < -0.03:  # 平仓 ,亏损或盈利达预期则平仓
            close_position(pos_data['posSide'])
        elif pos_data['posSide'] == 'long' and float(ma_small.iloc[8]) < float(ma_large.iloc[238]) and float(ma_small.iloc[9]) < float(ma_large.iloc[239]) and float(data1['close'].iloc[1]) > float(ma_small.iloc[8]) and float(data1['close'].iloc[0]) < float(ma_small.iloc[9]):
            close_position(pos_data['posSide'])
            # order_id = generate_order_id()
            # open_position('sell')
        elif pos_data['posSide'] == 'short' and float(ma_small.iloc[8]) > float(ma_large.iloc[238]) and float(ma_small.iloc[9]) > float(ma_large.iloc[239]) and float(data1['close'].iloc[1]) < float(ma_small.iloc[8]) and float(data1['close'].iloc[0]) > float(ma_small.iloc[9]):
            close_position(pos_data['posSide'])
            # order_id = generate_order_id()
            # open_position('buy')

def open_position(direction):
    global position_opened
    info = {}
    info['币种'] = dbz
    info['date'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    info['方向'] = "买" if direction == "buy" else "卖"
    info['状态'] = position_opened
    info['订单ID'] = order_id

    ye = account("USDT")
    ccb = ye["details"][0]["availBal"]
    cb = float(ccb) / 2
    if float(cb) >= 100:
        side = "buy" if direction == "buy" else "sell"
        posSide = "long" if direction == "buy" else "short"
        result = tradeAPI.place_order(instId=bz, tdMode="cross", posSide=posSide, side=side, clOrdId=direction+str(order_id), ordType="market", sz="300")
     
        print('--------------',result)
        position_opened = True
        oid = result['data'][0]['clOrdId']
        #print(oid)
        # 成交价
        bcj = getOrder(oid)['data'][0]['fillPx']
        print(bcj)
        # 订单手续费
        bsx = getOrder(oid)['data'][0]['fee']
        print(bsx)
        info['oid'] = "buy"+str(order_id)
        info['成交价'] = bcj
        info['资金费'] = bsx
        dd.append(info)
    else:
        print(f"\033[31m{direction}操作忽略,USDT余额不足\033[0m")

def close_position(posSide):
    global position_opened
    info = {}
    if posSide == "short":
        direction = "sell"
    else:
        direction = "buy"
    info['币种'] = dbz
    info['date'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
    info['方向'] = "平仓"
    info['状态'] = position_opened
    info['订单ID'] = direction+str(order_id)

    try:
        print(info)
        # print(direction+str(order_id))

        # print(getOrder(direction+str(order_id)))
        byex = getOrder(direction+str(order_id))['data'][0]['fillSz']
        
        
    except:
        print(f"\033[31m没有买入订单,忽略\033[0m")
        return

    if float(byex) != 0:
        uresult = tradeAPI.close_positions(instId=bz, clOrdId=direction+str(order_id), posSide=posSide, mgnMode="cross")
     
        print('++++++++++',uresult)
        position_opened = False
        uoid = uresult['data'][0]['clOrdId']
        info['uoid'] = uoid
        # 订单币币余额
        uye = getOrder(uoid)['data'][0]['fillSz']
        # 订单币币收入
        uxf = getOrder(uoid)['data'][0]['sz']
        # 成交价
        ucj = getOrder(uoid)['data'][0]['fillPx']
        # 订单手续费
        usx = getOrder(uoid)['data'][0]['fee']
            
        info['uoid'] = "sell"+str(order_id)
        info['成交价'] = ucj
        info['资金费'] = usx
        dd.append(info)
    else:
        print("\033[31msell操作忽略,BTC余额不足\033[0m")

if __name__ == "__main__":
    dd = []
    setGgbnum()
    position_opened = False
    while True:
        log_dictionary(dd)
        dd.clear()
        time.sleep(4)
        for attempt in range(3):
            try:
                jy()
            except Exception as e:
                print(f"Error timeout: {e}")
                if attempt < 4:
                    time.sleep(2)
                else:
                    print("Failed to execute trading logic after 3 attempts.")
                    exit(113)
      
        print("aaaaaaaaaaaaaa",position_opened)