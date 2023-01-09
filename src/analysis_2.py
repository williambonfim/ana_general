import pandas as pd
import datetime as dt
from Function import f

class Strat_opening():
    def __init__(self, symbol, tf, time, sl, date_0, buy = True):
        self.symbol = symbol
        self.tf = tf
        self.time = time
        self.sl = sl
        self.date_0 = date_0 = pd.to_datetime(date_0)
        self.buy = buy
    
    def check_strat(abc):
        if abc.buy:
            df = f.compile_df(abc.tf, abc.symbol, abc.time, abc.date_0)

            df['target'] = pd.Series(data=df['target'], index = df.index).mask(df['d_low'] <= -abc.sl, -abc.sl)
            df['target'] = pd.Series(data=df['target'], index = df.index).mask(~(df['d_low'] <= -abc.sl), df['d_close'])

            f.compile_results(df, abc.symbol, abc.tf)
        
        elif abc.buy == False:
            df = f.compile_df(abc.tf, abc.symbol, abc.time, abc.date_0)

            df['target'] = pd.Series(data=df['target'], index = df.index).mask(df['d_high'] >= abc.sl, -abc.sl)
            df['target'] = pd.Series(data=df['target'], index = df.index).mask(~(df['d_high'] >= abc.sl), -df['d_close'])

            f.compile_results(df, abc.symbol, abc.tf)


if __name__ == '__main__':
    # Analysis of opening an order with sl definied and closing order at definied time

    #=================INPUT=====================
    HKInd  = Strat_opening('HKInd', 'M15', '02:30', 1000, dt.date(2022,10,31), buy=True)
    HKInd2 = Strat_opening('HKInd', 'M15', '02:30', 1000, dt.date(2022,10,31), buy=False)
    HKInd3 = Strat_opening('HKInd', 'M30', '02:30', 500, dt.date(2022,10,31), buy=True)
    HKInd4 = Strat_opening('HKInd', 'M30', '02:30', 500, dt.date(2022,10,31), buy=False)
    
    UsaTec = Strat_opening('UsaTec', 'M15', '15:30', 500, dt.date(2022,10,31), buy=False)

    Usa500 = Strat_opening('Usa500', 'M15', '15:30', 100, dt.date(2022,10,31), buy=True)

    UsaInd = Strat_opening('UsaInd', 'M15', '15:30', 500, dt.date(2022,10,31), buy=True)
    UsaInd2 = Strat_opening('UsaInd', 'M15', '15:30', 500, dt.date(2022,10,31), buy=False)

    Ger401 = Strat_opening('Ger40', 'M15', '09:00', 500, dt.date(2022,10,31), buy=True)
    Ger402 = Strat_opening('Ger40', 'M15', '09:00', 500, dt.date(2022,10,31), buy=False)

    trades = [HKInd, HKInd2, HKInd3, HKInd4,
              UsaTec,
              Ger401, Ger402,
              Usa500,
              UsaInd, UsaInd2
             ]
    
    trades = [UsaInd, UsaInd2, HKInd, HKInd2]
    #===========================================
    for trade in trades:
        trade.check_strat()