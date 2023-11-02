import okx.Account as Account
import okx.Trade as Trade
import okx.MarketData as MarketData
import pandas as pd
import datetime
import json
import time

# API 初始化
apikey="1a191170-e307-41b3-a5b4-8a922a041bce"
secretkey="6AB88801ADB8F7CC0B8B209E54326623"
passphrase="Vevor@com123"

flag = "1"  # 实盘:0 , 模拟盘:1

accountAPI = Account.AccountAPI(apikey, secretkey, passphrase, False, flag)
tradeAPI = Trade.TradeAPI(apikey, secretkey, passphrase, False, flag)
marketDataAPI = MarketData.MarketAPI(flag=flag)
bz="ETH-USDT"
dbz="ETH"



def tradedata():
    result = tradeAPI.get_orders_history(
    instType="SPOT",
    ordType="market,post_only,fok,ioc"
)
    return result

def account(cb):
    result = accountAPI.get_account_balance(
        ccy=cb
    )
    return result["data"][0]
    

    
        


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








print("\033[34m~~~~~starting jy %s\033[0m"%dbz)



def jy():
 
    #---------测试代码
    # ye = account("USDT")
    # print(ye)
    # exit(1001)
    #--------------

    # 检查交叉点
    if short_moving_average.iloc[-1] > long_moving_average.iloc[-1] and short_moving_average.iloc[-2] <= long_moving_average.iloc[-2]:
        # 买入信号
        ye = account("USDT")
        print(ye)
        cb=ye["details"][0]["cashBal"]
        # print("----------------okkkkk")
        # exit(1001)
        if float(cb) > 10:
            result = tradeAPI.place_order(
                instId=bz,
                tdMode="cash",
                # clOrdId="buy_order_01",
                ccy="USDT",
                side="buy",
                ordType="market",
                sz=cb  # 买入100 USDT的BTC
                
            )           
            print("\033[32m++++hit++buy\033[0m")
            
        else:
            print("\033[31mbuy操作忽略,USDT余额不足\033[0m")
          

    elif short_moving_average.iloc[-1] < long_moving_average.iloc[-1] and short_moving_average.iloc[-2] >= long_moving_average.iloc[-2]:
        # 卖出信号
        ye = account(dbz)
        # print(ye)
        cb=ye["details"][0]["cashBal"]
        if ye["details"] != 0:
            result = tradeAPI.place_order(
                # instId="BTC-USDT",
                instId=bz,
                tdMode="cash",
                # clOrdId="sell_order",
                ccy=dbz,
                side="sell",
                ordType="market",
                sz=cb  # 卖出100 USDT的BTC
            )
            print("\033[32m---hit-----sell\033[0m")
            
        else:
            print("\033[31msell操作忽略,BTC余额不足\033[0m")
            
    else:
        print("\033[33m###########miss\033[0m")

if __name__=="__main__":

    while True:  
        # 获取历史数据
        historical_data = marketDataAPI.get_candlesticks(
            instId=bz,
            bar="1M"
        ) 

        result = marketDataAPI.get_history_candlesticks(
            instId=bz,
            bar="1H"
        )

        data = pd.DataFrame(historical_data["data"],columns=["ts","o","h","l","c","vol","volCcy","volCcyQuote","confirm"])
        # print(data["c"])  # 打印data的前5行以检查数据
        # 计算移动平均线
        short_moving_average = data['c'].astype(float).rolling(window=15).mean()  # 10 periods SMA
        long_moving_average = data['c'].astype(float).rolling(window=150).mean()  # 50 periods SMA

        print("%s\n%s\n%s\n%s"%(short_moving_average.iloc[-1],long_moving_average.iloc[-1],short_moving_average.iloc[-2],long_moving_average.iloc[-2]))
        time.sleep(3)
        jy()
