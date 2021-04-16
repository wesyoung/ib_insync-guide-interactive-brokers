import pandas as pd
from ib_insync import *

ib = IB()
ib.connect(clientId=8)


def new_data(tickers):
    global df

    ''' process incoming data and check for trade entry '''
    for ticker in tickers:
        df.loc[ticker.time] = ticker.last
    print(df)
    five_mins_ago = df.index[-1] - pd.Timedelta(seconds=60)

    if df.index[0] < five_mins_ago:
        df = df[five_mins_ago:]

        price_min = df._last.min()
        price_max = df._last.max()

        if df._last[-1] > price_min * 1.001:
            place_order('BUY')

        elif df._last[-1] < price_max * 0.999:
            place_order('SELL')


def place_order(direction):
    mastercard_order = MarketOrder(direction, 1)
    trade = ib.placeOrder(mastercard_contract, mastercard_order)
    ib.sleep(3)
    if trade.orderStatus.status == 'Filled':
        ib.disconnect()
        quit(0)


# init dataframe
df = pd.DataFrame(columns=['date', '_last'])
df.set_index('date', inplace=True)

# Create contracts
mastercard_contract = Stock('QQQ', 'SMART', 'USD')

ib.qualifyContracts(mastercard_contract)

# Request market data for Visa
ib.reqMktData(mastercard_contract)

# Set callback function for tick data
ib.pendingTickersEvent += new_data

# Run infinitely
ib.run()
