import okx.Account as Account
import okx.MarketData as MarketData
import configparser


# 配置文件读取API初始化信息
config = configparser.ConfigParser()
config.read('config.ini')

apikey = config['OKX']['apikey']
secretkey = config['OKX']['secretkey']
passphrase = config['OKX']['passphrase']
flag = config['OKX']['flag']  # 实盘:0 , 模拟盘:1

accountAPI = Account.AccountAPI(apikey, secretkey, passphrase, False, flag)
marketDataAPI = MarketData.MarketAPI(flag=flag)
bz = "BTC-USDT-SWAP"

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


def jy():
 
    a = getTicker()['data']
# 创建一个列表，存储交易对的ID和计算出的交易量
    trades = [(n['instId'], float(n['volCcy24h']) * float(n['last']) / 100000000) for n in a if "USDT" in n['instId'] \
              and float(n['volCcy24h']) * float(n['last']) / 100000000 > 2 and float(n['last']) > 0 ]

# 根据交易量对列表进行排序，降序排列
    sorted_trades = sorted(trades, key=lambda x: x[1], reverse=True)

# 打印排序后的交易对和交易量
    for instId, num in sorted_trades:
        print(instId, "---", round(num, 2), "亿")
    exit(1)
   


if __name__ == "__main__":
    jy()