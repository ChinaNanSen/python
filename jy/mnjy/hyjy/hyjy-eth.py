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
# from datetime import *


# API 初始化
# 从配置文件读取API初始化信息
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




def getOrder(oid):
    result = tradeAPI.get_order(
        instId=bz,
        # ordId=oid,
        clOrdId=oid
    )
    time.sleep(0.1)
    return result


def generate_order_id():
    # 生成一个新的随机订单号
    return random.randint(10000, 99999)


def tradedata():
    result = tradeAPI.get_orders_history(
        instType="SPOT",
        ordType="market,post_only,fok,ioc"
    )
    time.sleep(0.1)
    return result

def positions():
    result = accountAPI.get_positions(
        instType="SWAP",
        instId=bz
    )
    time.sleep(0.1)
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
            time.sleep(0.1)
            return result["data"][0]
        except Exception as e:
            print(f"Error: {e}")
            if attempt < 2:  # 如果这不是最后一次尝试，等待2秒然后再次尝试
                time.sleep(2)
            else:
                print("Failed to get account balance after 3 attempts.")
                return None  # 或者返回一个错误值/异常，让调用者知道请求失败


# # 获取历史数据
# historical_data = marketDataAPI.get_candlesticks(
#     instId="BTC-USDT",
#     # bar="5m"
# )
"""
bar	String	否	时间粒度，默认值1m
如 [1m/3m/5m/15m/30m/1H/2H/4H]
香港时间开盘价k线：[6H/12H/1D/2D/3D/1W/1M/3M]
UTC时间开盘价k线：[/6Hutc/12Hutc/1Dutc/2Dutc/3Dutc/1Wutc/1Mutc/3Mutc]
"""

# 转换数据到 DataFrame

"""
ts	String	开始时间，Unix时间戳的毫秒数格式，如 1597026383085
o	String	开盘价格
h	String	最高价格
l	String	最低价格
c	String	收盘价格
vol	String	交易量，以张为单位
如果是衍生品合约，数值为合约的张数。
如果是币币/币币杠杆，数值为交易货币的数量。
volCcy	String	交易量，以币为单位
如果是衍生品合约，数值为交易货币的数量。
如果是币币/币币杠杆，数值为计价货币的数量。
volCcyQuote	String	交易量，以计价货币为单位
如：BTC-USDT 和 BTC-USDT-SWAP, 单位均是 USDT；
BTC-USD-SWAP 单位是 USD
confirm	String	K线状态
0 代表 K 线未完结，1 代表 K 线已完结。

"""


print("\033[34m~~~~~starting jy %s\033[0m" % dbz)



def jy():

    # 跟踪全局变量状态
    global position_opened
    global order_id  # 使用global关键字声明order_id是全局变量
    
    # print(getOrder('641999281087422464'))
    # exit(1006)
  

   # 获取当前时间的 Unix 时间戳
    timestamp = time.time()
    local_time = time.localtime(timestamp)
    nows = time.asctime(local_time)
    time_tuple = time.strptime(nows, "%a %b %d %H:%M:%S %Y")
    now = time.strftime("%Y-%m-%d %H:%M:%S", time_tuple)

        
    # 获取历史数据
    historical_data = marketDataAPI.get_candlesticks(
        instId=bz,
        # before="",
        # bar="30m",
        bar="6H",
        limit="160"
    )
    time.sleep(0.1)
    data1 = pd.DataFrame(historical_data["data"], columns=[
        "ts", "open", "high", "low", "close", "vol", "volCcy", "volCcyQuote", "confirm"])

    data1['ts'] = data1['ts'].apply(
        lambda x: datetime.datetime.fromtimestamp(int(x) / 1000))
    data1['ts'] = data1['ts'].dt.strftime('%Y-%m-%d %H:%M:%S')
    data1.set_index('ts', inplace=True)

    ma15 = finta.TA.SMA(data1, 15)
    ma150 = finta.TA.SMA(data1, 150)
    bmacd = finta.TA.MACD(data1,13,34)
    ma = ma150.iloc[149]
    bbands = finta.TA.BBANDS(data1)
    bu = bbands.iloc[19]['BB_UPPER']
    bm = bbands.iloc[19]['BB_MIDDLE']
    bl = bbands.iloc[19]['BB_LOWER']
    cn = data1['close'].iloc[0]
    hn = data1['high'].iloc[0]
    ln = data1['low'].iloc[0]
    ema10 = finta.TA.EMA(data1,10)
    ema30 = finta.TA.EMA(data1,30)
    # print(bmacd)
    # print(bmacd['macd'].iloc[0])
    # exit(1)

    # print("%s\n%s\n" %
    #       (ma15.iloc[15], ma150.iloc[150]))
    # print("ma150: ",ma)
    # print("cn: ",cn)
    # print("================")
    # print("ln:%s\nbl:%s\n" %(ln, bl))
    # print("-------------")
    # print("hn:%s\nbu:%s\n" %(hn, bu))


    # 检查交叉点并执行交易逻辑
    buy_signals = {}
    sell_signals = {}
    


    # if ma15.iloc[15] > ma150.iloc[150] and position_opened:
    # cz = float(bl) - float(ln)
    # print("cz: ",cz)
    if  position_opened == False and bmacd['macd'].iloc[1] < 0 and  bmacd['macd'].iloc[0] > 0  and ema30.iloc[0] > ema10.iloc[0]:
    # if float(cn) > ma and float(ln) < bl and  cz > 10 and position_opened == False:

    # if float(ln) < bl and position_opened:

        order_id = generate_order_id()
        print("\033[32m开始买入\033[0m")
        print("-----")
        
        # 买入信号
        
        ye = account("USDT")
        

        ccb = ye["details"][0]["availBal"]
        cb = float(ccb) / 2
        # print(ye)
        print(position_opened)
        # exit(1023)
        print(cb)
        info = {}
        info['币种'] = dbz 
        info['date'] = now
        info['方向'] = "买"
        info['状态'] = position_opened
        info['订单ID'] = order_id
        info['支出'] = cb
        info['最低价'] = ln
        info['LB'] = bl
       
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
                sz="400"  # 买入100 USDT的BTC
            )
            time.sleep(0.1)
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
            
            info['oid'] = "buy"+str(order_id)
            info['成交价'] = bcj
            info['资金费'] = bsx
            dd.append(info)
            # print(dd)

            buy_signals[data1.index[15]] = data1['close'].iloc[15]
            print("\033[32m++++hit++buy\033[0m")
        else:
            print("\033[31mbuy操作忽略,USDT余额不足\033[0m")

    # elif ma15.iloc[15] < ma150.iloc[150] and position_opened == False:
    # zc = float(hn) - float(bu)
    # print("zc: ",zc)
    if position_opened and bmacd['macd'].iloc[1] > 0 and  bmacd['macd'].iloc[0] < 0  and ema30.iloc[0] < ema10.iloc[0]:
    # if float(hn) > bu and zc > 5 and position_opened:
        print("\033[31m开始卖出\033[0m")
        print("++++++++++")
        print(order_id)
        info = {}
        info['币种'] = dbz
        info['date'] = now
        info['方向'] = "卖"
        info['状态'] = position_opened
        info['订单ID'] = order_id
        # info['支出'] = cb
        info['最高价'] = hn
        info['UB'] = bu
    
        # 卖出信号
        try:
            byex = getOrder("buy"+str(order_id))['data'][0]['fillSz']
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
            time.sleep(0.1)
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
            
            info['uoid'] = "sell"+str(order_id)
            info['成交价'] = ucj
            info['资金费'] = usx
            dd.append(info)

            sell_signals[data1.index[15]] = data1['close'].iloc[15]
            print("\033[32m---hit-----sell\033[0m")

        else:
            print("\033[31msell操作忽略,BTC余额不足\033[0m")
    else:
        print("\033[33m###########miss\033[0m")


    if position_opened:
        print(position_opened)
        pos_data = positions()['data'][0]
        if float(pos_data['upl']) <= -9:
            print("\033[31m亏损超过9U,平仓\033[0m")
            print(order_id)
            print("==========")
            info = {}
            info['币种'] = dbz
            info['date'] = now
            info['方向'] = "平仓"
            info['状态'] = position_opened
            info['订单ID'] = order_id
            info['亏损'] = pos_data['upl']
            
            # 卖出信号
            try:
                byex = getOrder("buy"+str(order_id))['data'][0]['fillSz']
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
               
                info['id'] = "sell"+str(order_id)
                info['成交价'] = ucj
                info['资金费'] = usx
                dd.append(info)
               

                sell_signals[data1.index[15]] = data1['close'].iloc[15]
                print("\033[32m---hit-----sell\033[0m")
                time.sleep(240)

            else:
                print("\033[31msell操作忽略,BTC余额不足\033[0m")



if __name__ == "__main__":
    dd = []  
    position_opened = False
    while True:
        # print(dd)
        # 将交易记录输出到文件
        log_dictionary(dd)
        dd.clear()
        time.sleep(4)
        for attempt in range(3):  # 尝试次数
            try:
                jy()
            except Exception as e:
                print(f"Error timeout: {e}")
                if attempt < 4:  # 如果这不是最后一次尝试，等待2秒然后再次尝试
                    time.sleep(2)
                else:
                    print("Failed to execute trading logic after 3 attempts.")
                    exit(113)
                
        time.sleep(0.1)
        print(position_opened)
        
        
        