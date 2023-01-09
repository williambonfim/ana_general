import pandas as pd

class f():
    def compile_df(tf, symbol, time, date_0):
        df = pd.read_csv('/Volumes/PiNAS/market/Data_MT5/{}_{}.csv'.format(tf, symbol))

        df['time'] = pd.to_datetime(df['time'])
        df.set_index('time', inplace=True)

        df = df[~(df.index < date_0)]
        df.drop(['tick_volume', 'spread', 'real_volume'], axis=1, inplace=True)

        df = df.between_time(time, time)

        df['d_high'] =   ((df['high'] - df['open']) * 100).astype('int')
        df['d_low'] =     ((df['low'] - df['open']) * 100).astype('int')
        df['d_close'] = ((df['close'] - df['open']) * 100).astype('int')
        df['target'] = 0

        return df

    def compile_df_range(tf, symbol, time_0, time_1, date_0):
        # Read data from csv data saved on my local NAS
        df = pd.read_csv('/Volumes/PiNAS/market/Data_MT5/{}_{}.csv'.format(tf, symbol))

        # Drop columns that will not be used
        df.drop(['tick_volume', 'spread', 'real_volume'], axis=1, inplace=True) 

        # Set the time column to Pandas datetime and set the time as index 
        df['time'] = pd.to_datetime(df['time'])
        df.set_index('time', inplace=True)

        # Get the data from initial date_0
        df = df[~(df.index < date_0)]

        # Get the data between time_0 and time_1
        df = df.between_time(time_0, time_1)

        df['p_high'] =   ((df['high'] - df['open']) / df['open'])
        df['p_low'] =     ((df['low'] - df['open']) / df['open'])
        df['p_close'] = ((df['close'] - df['open']) / df['open'])
        
        return df

    def compile_results(df, symbol, tf):
        system_result = df.sum()['d_close']
        result_test = df.sum()['target']

        count_tp = df[df['target'] > 0].count()['target']
        count_trades = df.astype(bool).sum(axis=0)['target']
        print()
        print('===================================================')
        print(f'{symbol}-{tf}')
        print(df)
        print()
        print('Compra e venda no fechamento da barra: ',system_result)
        print()
        print('Resultado total: ',result_test)
        print('No. acertos: ',count_tp)
        print('No. trades: ',count_trades)
        print('% acertos: ',count_tp/count_trades*100)