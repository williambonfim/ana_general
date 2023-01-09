import pandas as pd
import datetime as dt
from Function import f
            
class Strat_opening_tp_sl():
    def __init__(self, symbol, tf, time, sl, tp, date_0, buy = True):
        self.symbol = symbol
        self.tf = tf
        self.time = time
        self.sl = sl
        self.tp = tp
        self.date_0 = date_0 = pd.to_datetime(date_0)
        self.buy = buy
    
    def check_strat(abc):
        if abc.buy:
            df = f.compile_df(abc.tf, abc.symbol, abc.time, abc.date_0)

            df['target'] = pd.Series(data=df['target'], index = df.index).mask(df['d_high'] >= abc.tp, abc.tp)
            df['target'] = pd.Series(data=df['target'], index = df.index).mask(~(df['d_high'] >= abc.tp), df['d_low'])
            df['target'] = pd.Series(data=df['target'], index = df.index).mask((df['target'] < -abc.sl), -abc.sl)

            f.compile_results(df, abc.symbol, abc.tf)
            
        
        elif abc.buy == False:
            df = f.compile_df(abc.tf, abc.symbol, abc.time, abc.date_0)

            df['target'] = pd.Series(data=df['target'], index = df.index).mask(df['d_low'] <= -abc.tp, abc.tp)
            df['target'] = pd.Series(data=df['target'], index = df.index).mask(~(df['d_low'] <= -abc.tp), -df['d_high'])
            df['target'] = pd.Series(data=df['target'], index = df.index).mask((df['target'] < -abc.sl), -abc.sl)

            f.compile_results(df, abc.symbol, abc.tf)

if __name__ == '__main__':
    # Analysis of opening an order at a time with a sl and tp definied

    #=================INPUT=====================
    HKInd = Strat_opening_tp_sl('HKInd', 'M15', '02:30', 6000, 3000, dt.date(2022,10,31), True)
    UsaTec = Strat_opening_tp_sl('UsaTec', 'M15', '15:30', 1500, 1000, dt.date(2022,10,31), False)
    Ger40 = Strat_opening_tp_sl('Ger40', 'M15', '09:00', 1500, 1000, dt.date(2022,10,31), True)

    trades = [HKInd,
              Ger40,
              UsaTec,
             ]
    
    #===========================================
    for trade in trades:
        trade.check_strat()