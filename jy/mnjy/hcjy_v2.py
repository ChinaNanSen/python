import pandas as pd
import finta
import ccxt
from datetime import datetime
import time

def get_historical_data(symbol, start_date, end_date, timeframe):
    """
    从 CCXT 获取指定时间段的历史 K 线数据
    """
    exchange = ccxt.okx()

    # 将字符串日期转换为毫秒时间戳
    start_ts = int(datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S').timestamp() * 1000)
    end_ts = int(datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S').timestamp() * 1000)

    # 获取历史数据
    all_ohlcv = []
    while start_ts < end_ts:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since=start_ts)
        if not ohlcv:
            break
        # 过滤并处理数据
        for row in ohlcv:
            if row[0] < end_ts:
                all_ohlcv.append(row)
            else:
                # 一旦发现数据超出结束时间，立即停止添加
                break
        
        # 更新开始时间戳为最后一条数据的时间加上时间框架
        start_ts = ohlcv[-1][0] + exchange.parse_timeframe(timeframe) * 1000
        time.sleep(exchange.rateLimit / 1000)

    return pd.DataFrame(all_ohlcv, columns=["ts", "open", "high", "low", "close", "vol"])

def backtest(data, capital, strategy_params):
    # 定义手续费和滑点
    commission_rate = 0.001
    slippage = 0.0005

    # 初始化账户余额和持仓
    balance = capital
    position = 0
    total_commission = 0  # 总手续费

    # 添加技术指标
    data['ma_small'] = finta.TA.SMA(data, 10)
    data['ma_large'] = finta.TA.SMA(data, 60)

    # 记录交易信息
    trades = []

    for i in range(10, len(data)):
        # 根据策略信号进行买入/卖出操作
        if position == 0:
            if data.loc[data.index[i], 'close'] < data.loc[data.index[i], 'ma_small'] and \
                    data.loc[data.index[i-1], 'close'] > data.loc[data.index[i-1], 'ma_small']:
                # 买入信号
                trade_price = data.loc[data.index[i], 'close'] * (1 + slippage)
                trade_amount = balance / trade_price
                fee = trade_amount * trade_price * commission_rate
                balance -= trade_amount * trade_price + fee
                position += trade_amount
                total_commission += fee  # 累加手续费
                trades.append({'datetime': data.index[i], 'type': 'buy', 'price': trade_price,
                               'amount': trade_amount, 'fee': fee, 'cash': balance, 'position': position})
            elif data.loc[data.index[i], 'close'] > data.loc[data.index[i], 'ma_small'] and \
                    data.loc[data.index[i-1], 'close'] < data.loc[data.index[i-1], 'ma_small']:
                # 卖出信号
                trade_price = data.loc[data.index[i], 'close'] * (1 - slippage)
                trade_amount = balance / trade_price
                balance += trade_amount * trade_price
                position = -trade_amount
                trades.append({'datetime': data.index[i], 'type': 'sell', 'price': trade_price,
                               'amount': trade_amount, 'fee': 0, 'cash': balance, 'position': position})
        elif position > 0:
            if data.loc[data.index[i], 'close'] > data.loc[data.index[i], 'ma_small'] and \
                    data.loc[data.index[i-1], 'close'] < data.loc[data.index[i-1], 'ma_small']:
                # 卖出信号
                trade_price = data.loc[data.index[i], 'close'] * (1 - slippage)
                fee = position * trade_price * commission_rate
                balance += position * trade_price - fee
                total_commission += fee  # 累加手续费
                position = 0
                trades.append({'datetime': data.index[i], 'type': 'sell', 'price': trade_price,
                               'amount': position, 'fee': fee, 'cash': balance, 'position': position})
        else:
            if data.loc[data.index[i], 'close'] < data.loc[data.index[i], 'ma_small'] and \
                    data.loc[data.index[i-1], 'close'] > data.loc[data.index[i-1], 'ma_small']:
                # 买入信号
                trade_price = data.loc[data.index[i], 'close'] * (1 + slippage)
                trade_amount = balance / trade_price
                fee = trade_amount * trade_price * commission_rate
                balance -= trade_amount * trade_price + fee
                position -= trade_amount
                total_commission += fee  # 累加手续费
                trades.append({'datetime': data.index[i], 'type': 'buy', 'price': trade_price,
                               'amount': trade_amount, 'fee': fee, 'cash': balance, 'position': position})

    # 计算最终资产价值
    final_balance = balance + abs(position) * data['close'].iloc[-1]
    performance = final_balance - capital

    # 将交易记录输出到文件
    trades_df = pd.DataFrame(trades)
    trades_df.to_csv('trading_record.csv', index=False)

    # 打印结果
    print(f"Initial Balance: {capital}, Final Balance: {final_balance}, Performance: {performance}, Total Commission Paid: {total_commission}")

    return trades_df

if __name__ == "__main__":
    # 设置回测参数
    symbol = 'BTC/USDT'
    start_date = '2023-05-01 00:00:00'
    end_date = '2023-05-31 23:59:59'
    timeframe = '5m'
    initial_capital = 1000

    # 获取历史数据
    data = get_historical_data(symbol, start_date, end_date, timeframe)
    data['ts'] = pd.to_datetime(data['ts'], unit='ms')
    data.set_index('ts', inplace=True)

    # 运行回测
    trades_df = backtest(data, initial_capital, {})