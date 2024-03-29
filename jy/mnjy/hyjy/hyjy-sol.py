import okx.Account as Account
import okx.Trade as Trade
import okx.MarketData as MarketData
import pandas as pd
import datetime
import json
import time
import finta
import configparser
import random
import httpx  # 导入httpx用于异常处理
import ccxt

# API 初始化
config = configparser.ConfigParser()
config.read('config.ini')

apikey = config['OKX']['apikey']
secretkey = config['OKX']['secretkey']
passphrase = config['OKX']['passphrase']
flag = config['OKX']['flag']  # 实盘:0 , 模拟盘:1

accountAPI = Account.AccountAPI(apikey, secretkey, passphrase, False, flag)
tradeAPI = Trade.TradeAPI(apikey, secretkey, passphrase, False, flag)
marketDataAPI = MarketData.MarketAPI(flag=flag)
bz = "SOL-USDT-SWAP"
dbz = "SOL"

# 其余函数保持不变...
def getOrder(oid):
    # 获取订单详情
    result = tradeAPI.get_order(
        instId=bz,
        # ordId=oid,
        clOrdId=oid
    )
    return result

def generate_order_id():
    # 生成随机订单号
    return random.randint(10000, 99999)

def positions():
    # 获取当前头寸
    return accountAPI.get_positions(instType="SWAP", instId=bz)

def account_balance(currency):
    # 获取账户余额
    try:
        result = accountAPI.get_account_balance(ccy=currency)
        return result["data"][0]
    except Exception as e:
        print(f"Error getting account balance: {e}")
        return None
    


def get_historical_datas():
    #获取历史数据
    try:
        historical_data = marketDataAPI.get_candlesticks(
            instId=bz,
            bar="30m", 
            limit="160")
        time.sleep(0.1)
        return pd.DataFrame(historical_data["data"], columns=[
            "ts", "open", "high", "low", "close", "vol", "volCcy", "volCcyQuote", "confirm"])
    except httpx.HTTPError as e:
        print(f"网络请求错误: {e}")
        return None
    

def get_historical_data():
    
    exchange = ccxt.okx()

    # 设置交易对和时间框架
    symbol = dbz+'/USDT'  # 比特币与USDT的交易对
    # print(symbol)
    timeframe = '30m'  # 时间框架

    # 获取历史数据
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe)

    time.sleep(exchange.rateLimit / 1000)

    return pd.DataFrame(ohlcv, columns=["ts", "open", "high", "low", "close", "vol"])


# 其余函数保持不变...
def process_data(data_frame):
    # 处理数据
    data_frame['ts'] = data_frame['ts'].apply(
        lambda x: datetime.datetime.fromtimestamp(int(x) / 1000))
    data_frame['ts'] = data_frame['ts'].dt.strftime('%Y-%m-%d %H:%M:%S')
    data_frame.set_index('ts', inplace=True)
    return data_frame

def trading_logic(data_frame, data_frames, position_opened):
    
    # 交易逻辑
    ma15 = finta.TA.SMA(data_frame, 15)
    ma150 = finta.TA.SMA(data_frame, 150)
    bbands = finta.TA.BBANDS(data_frame)
    bu = bbands.iloc[-1]['BB_UPPER']
    bl = bbands.iloc[-1]['BB_LOWER']
    cn = data_frame['close'].iloc[-1]
    hn = data_frame['high'].iloc[-1]
    ln = data_frame['low'].iloc[-1]
    
    # print(data_frame)
    # print(ln)
    # print(hn)
    # exit(112)
    print("\033[32mln:%s\nbl:%s\n\033[0m" %(lns, bl))
    print("-------------")
    print("\033[31mhn:%s\nbu:%s\n\033[0m" %(hns, bu))
  

    if float(lns) < bl and  position_opened == False:
        print(position_opened)
        print("\033[32m开始买入\033[0m")
        return "buy"
    elif float(hns) > bu and position_opened:
        print("\033[31m开始卖出\033[0m")
        return "sell"
    elif position_opened:    
        pos_data = positions()['data'][0]
        print(pos_data['upl'])
        if float(pos_data['upl']) <= -10:   
            print("\033[31m亏损超过10U,平仓\033[0m")
            return "sell"
    else:
        return "hold"

def execute_trade(trade_type, order_id):
    # 执行交易
    if trade_type == "buy":
        # 买入逻辑
        print(order_id)

        print("-----")
        # 买入信号
        ye = account_balance("USDT")
        ccb = ye["details"][0]["availBal"]
        cb = float(ccb) / 2
        
        # exit(1036)
        if float(cb) >= 100:
            result = tradeAPI.place_order(
                instId=bz,
                tdMode="cross",  # 保证金模式：isolated：逐仓 ；cross：全仓
                # ccy=dbz,
                # posSide="short",  # 选择 long 或 short
                # side="sell",
                posSide="long",  # 选择 long 或 short
                side="buy",
                clOrdId="buy"+str(order_id),
                ordType="market",  # market 市价单 ，limit 限价单
                # px="34430",
                sz="30"  # 买入100 USDT的BTC
            )
            print(result)
            # 更新持仓状态
            position_opened = True
            # 订单ID
            oid = result['data'][0]['clOrdId']
            # print(">>>>>>>>",oid)
            oidict = {}
            # 订单币币余额
            bye = getOrder(oid)['data'][0]['fillSz']
            # print(position_opened,"----------------",bye)
            # 订单币币余额消费
            bxf = getOrder(oid)['data'][0]['sz']
            # 成交价
            bcj = getOrder(oid)['data'][0]['fillPx']
            # 订单手续费
            bsx = getOrder(oid)['data'][0]['fee']
            oidict['oid'] = "buy"+str(order_id)
            oidict['bye'] = bye
            oidict['bxf'] = bxf
            oidict['bcj'] = bcj
            oidict['bsx'] = bsx
            print("\033[32m++++hit++buy\033[0m")
        else:
            print("\033[31mbuy操作忽略,USDT余额不足\033[0m")
        pass
    elif trade_type == "sell":
        # 卖出逻辑
        
        print("++++++++++")
        print(order_id)
        # 卖出信号
        try:
            byex = getOrder("buy"+str(order_id))['data'][0]['fillSz']
            # byex = getOrder("buy"+str(order_id))
            # print(byex)
            # exit(111)
        except Exception as es:
            print(f"\033[31m没有买入订单,忽略: {es} {byex}\033[0m")
        if float(byex) != 0:
            uresult = tradeAPI.close_positions(
                instId=bz,
                # ccy='BTC',
                clOrdId="sell"+str(order_id),
                posSide="long",
                mgnMode="cross"
            )
            print(uresult)
            position_opened = False
            uoid = uresult['data'][0]['clOrdId']
            print(uoid)
            # 订单币币余额
            uye = getOrder(uoid)['data'][0]['fillSz']
            # 订单币币收入
            uxf = getOrder(uoid)['data'][0]['sz']
            # 成交价
            ucj = getOrder(uoid)['data'][0]['fillPx']
            # 订单手续费
            usx = getOrder(uoid)['data'][0]['fee']
            # oidict['uoid'] = "sell"+str(order_id)
            # oidict['ubye'] = uye
            # oidict['ubxf'] = uxf
            # oidict['ubcj'] = ucj
            # oidict['ubsx'] = usx
            print("\033[32m---hit-----sell\033[0m")
        else:
            print("\033[31msell操作忽略,BTC余额不足\033[0m")
    else:
        print("\033[33m###########miss\033[0m")

def main():
    global position_opened
    current_order_id = None
    position_opened = False
    print("\033[34m~~~~~starting jy %s\033[0m" % dbz)
    retry_count = 0  # 重试计数器
    max_retries = 3  # 最大重试次数

    while True:
        time.sleep(2)  # 添加延迟以避免请求过于频繁
        data_frame = get_historical_data()
        data_frames = get_historical_datas()


        if data_frame is None:
            retry_count += 1
            if retry_count >= max_retries:
                print("达到最大重试次数，终止程序")
                break
            continue

        # 重置重试计数器
        retry_count = 0

        processed_data = process_data(data_frame)
        trade_type = trading_logic(processed_data, data_frames, position_opened)

        if trade_type == "buy":
            current_order_id = generate_order_id()
            execute_trade(trade_type, current_order_id)
            position_opened = True
        elif trade_type == "sell" and current_order_id is not None:
            execute_trade(trade_type, current_order_id)
            position_opened = False
            current_order_id = None

        print("当前持仓状态:", position_opened)

if __name__ == "__main__":
    main()
