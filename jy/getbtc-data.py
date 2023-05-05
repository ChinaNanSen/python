import ccxt
import config

symbol = 'BTC/USDT'

def get_live_data():
    exchange = ccxt.okex({
        'apiKey': config.api_key,
        'secret': config.secret_key,
        'password': config.password,
        'enableRateLimit': True,
    })

    ticker = exchange.fetch_ticker(symbol)
    return ticker

if __name__ == "__main__":
    live_data = get_live_data()
    print(live_data)
