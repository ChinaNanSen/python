import okx.Account as Account
import okx.Trade as Trade
import okx.MarketData as MarketData
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import json
import time
import finta
import configparser
import random


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
bz = "ETH-USDT"
dbz = "ETH"


# 设置字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体为黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题


def tradedata():
    result = tradeAPI.get_orders_history(
        instType="SPOT",
        ordType="market,post_only,fok,ioc"
    )
    return result


# def account(cb):
#     result = accountAPI.get_account_balance(
#         ccy=cb
#     )
#     return result["data"][0]


# 通过 ordId 查询订单

def getOrder(oid):
    result = tradeAPI.get_order(
        instId=bz,
        # ordId=oid,
        clOrdId=oid
    )
    return result


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


def generate_order_id():
    # 生成一个新的随机订单号
    return random.randint(10000, 99999)


# # 获取历史数据
# historical_data = marketDataAPI.get_candlesticks(
#     instId="BTC-USDT",
#     # bar="5m"
# )
"""
bar	String	否	时间粒度,默认值1m
如 [1m/3m/5m/15m/30m/1H/2H/4H]
香港时间开盘价k线:[6H/12H/1D/2D/3D/1W/1M/3M]
UTC时间开盘价k线:[/6Hutc/12Hutc/1Dutc/2Dutc/3Dutc/1Wutc/1Mutc/3Mutc]
"""

# 转换数据到 DataFrame

"""
ts	String	开始时间,Unix时间戳的毫秒数格式,如 1597026383085
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
如:BTC-USDT 和 BTC-USDT-SWAP, 单位均是 USDT;
BTC-USD-SWAP 单位是 USD
confirm	String	K线状态
0 代表 K 线未完结,1 代表 K 线已完结。

"""


print("\033[34m~~~~~starting jy %s\033[0m" % dbz)


def plot_data(data, ma15, ma150, buy_signals, sell_signals):
    plt.figure(figsize=(12, 6))

    # 绘制收盘价格
    plt.plot(data.index, data['close'], label='价格', alpha=0.5)

    # 绘制移动平均线
    plt.plot(ma15.index, ma15, label='15周期简单移动平均线', alpha=0.9)
    plt.plot(ma150.index, ma150, label='150周期简单移动平均线', alpha=0.9)

    # 绘制买卖信号
    for date, price in buy_signals.items():
        plt.plot(date, price, 'o', markersize=10, label='买信号' if date ==
                 list(buy_signals.keys())[0] else "", color='g')
    for date, price in sell_signals.items():
        plt.plot(date, price, 'o', markersize=10, label='卖信号' if date ==
                 list(sell_signals.keys())[0] else "", color='r')

    plt.legend(loc='best')
    plt.title('价格、移动平均线和买卖信号')
    plt.xlabel('日期')
    plt.ylabel('价格')
    plt.grid()
    plt.show()


def jy():
    # 跟踪全局变量状态
    global position_opened
    global order_id  # 使用global关键字声明order_id是全局变量

    for attempt in range(3):  # 尝试次数
        try:
            # 获取历史数据
            historical_data = marketDataAPI.get_candlesticks(
                instId=bz,
                # before="",
                # bar="15m",
                limit="160"
            )

            data1 = pd.DataFrame(historical_data["data"], columns=[
                "ts", "open", "high", "low", "close", "vol", "volCcy", "volCcyQuote", "confirm"])

            data1['ts'] = data1['ts'].apply(
                lambda x: datetime.datetime.fromtimestamp(int(x) / 1000))
            data1['ts'] = data1['ts'].dt.strftime('%Y-%m-%d %H:%M:%S')
            data1.set_index('ts', inplace=True)

            ma15 = finta.TA.SMA(data1, 15)
            ma150 = finta.TA.SMA(data1, 150)
            bmacd = finta.TA.MACD(data1)
            bbands = finta.TA.BBANDS(data1)
            bu = bbands.iloc[-1]['BB_UPPER']
            bm = bbands.iloc[-1]['BB_MIDDLE']
            bl = bbands.iloc[-1]['BB_LOWER']

            # print(bmacd)
            # exit(1003)

            print("%s\n%s\n" %
                  (ma15.iloc[15], ma150.iloc[150]))
            cn = data1['close'].iloc[0]
            # print(type(cn))
            # print(type(bl))
            # exit(1024)
            # 检查交叉点并执行交易逻辑
            buy_signals = {}
            sell_signals = {}

            if float(cn) < bl and position_opened:

                # byex=getOrder("buy"+str(n))['data'][0]['fillSz']
                # print(byex)
                # exit(105)
                # 买入信号
                ye = account("USDT")

                ccb = ye["details"][0]["availBal"]
                cb = float(ccb) / 2

                # print(ye)

                # exit(104)

                if float(cb) > 10:
                    order_id = generate_order_id()
                    print(order_id)
                    result = tradeAPI.place_order(
                        instId=bz,
                        tdMode="cash",
                        clOrdId="buy"+str(order_id),
                        ccy="USDT",
                        side="buy",
                        ordType="market",
                        sz=cb  # 买入100 USDT的BTC

                    )
                    buy_signals[data1.index[15]] = data1['close'].iloc[15]

                    # print("+++++++++++",result)
                    # 更新持仓状态
                    position_opened = False
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
                    dd.append(oidict)
                    # exit(103)

                    print("\033[32m++++hit++buy\033[0m")
                else:
                    print("\033[31mbuy操作忽略,USDT余额不足\033[0m")

            elif float(cn) > bu and position_opened == False:
                print(order_id)
                # 卖出信号
                # ye = account(dbz)

                # cb = ye["details"][0]["availBal"]
                try:
                    byex = getOrder("buy"+str(order_id))['data'][0]['fillSz']
                except Exception as es:
                    print(f"\033[31m没有买入订单,忽略: {es} {byex}\033[0m")
                    break

                if float(byex) != 0:
                    uresult = tradeAPI.place_order(
                        instId=bz,
                        tdMode="cash",
                        clOrdId="sell"+str(order_id),
                        ccy=dbz,
                        side="sell",
                        ordType="market",
                        sz=byex  # 卖出100 USDT的BTC
                    )
                    print(uresult)
                    # 更新持仓状态
                    position_opened = True

                    sell_signals[data1.index[15]] = data1['close'].iloc[15]

                    uoid = uresult['data'][0]['ordId']
                    print(uoid)
                    # 订单币币余额
                    uye = getOrder(uoid)['data'][0]['fillSz']
                    # 订单币币收入
                    uxf = getOrder(uoid)['data'][0]['sz']
                    # 成交价
                    ucj = getOrder(uoid)['data'][0]['fillPx']
                    # 订单手续费
                    usx = getOrder(uoid)['data'][0]['fee']
                    oidict['uoid'] = "sell"+str(order_id)
                    oidict['ubye'] = uye
                    oidict['ubxf'] = uxf
                    oidict['ubcj'] = ucj
                    oidict['ubsx'] = usx
                    dd.append(oidict)
                    # exit(103)

                    print("\033[32m---hit-----sell\033[0m")
                else:
                    print("\033[31msell操作忽略,BTC余额不足\033[0m")
            else:
                print("\033[33m###########miss\033[0m")

            # 画图功能
            # plot_data(data1, ma15, ma150, buy_signals, sell_signals)

            # 如果代码运行成功，跳出循环
            break
        except Exception as e:
            print(f"Error: {e}")
            if attempt < 5:  # 如果这不是最后一次尝试，等待2秒然后再次尝试
                time.sleep(2)
            else:
                print("Failed to execute trading logic after 3 attempts.")


if __name__ == "__main__":
    dd = []

    position_opened = True
    while True:

        time.sleep(3)
        jy()
        print(position_opened)

        # print(dd)
    # 将交易记录输出到文件
    # trades_df = pd.DataFrame(dd)
    # trades_df.to_csv('bb_trading_record.csv', index=False)

