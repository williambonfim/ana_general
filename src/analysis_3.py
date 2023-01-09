import pandas as pd
import numpy as np
import datetime as dt
import pickle
from collections import Counter

from sklearn import svm, neighbors
from sklearn.model_selection import train_test_split
from sklearn.ensemble import VotingClassifier, RandomForestClassifier

def compile_df(tf, symbol, time_0, time_1, date_0):
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

        df.fillna(0, inplace=True)
        
        df.drop(['open', 'high', 'low', 'close'], axis=1, inplace=True)

        return df

def extract_futuresets(tf, symbol, time_0, time_1, date_0):
    date_0 = pd.to_datetime(date_0)

    df = compile_df(tf, symbol, time_0, time_1, date_0)

    df['target'] = list(map(buy_sell_hold,
                            df['p_close']
                            ))
    
    df['target'] = df.target.shift(-1)
    
    vals = df['target'].values.tolist()
    str_vals = [str(i) for i in vals]
    print(f'Data spread:', Counter(str_vals))

    df.fillna(0, inplace=True)
    df = df.replace([np.inf, -np.inf], np.nan)
    df.dropna(inplace=True)

    df_vals = df[['p_high', 'p_low', 'p_close']]
    df['target'] = df['target'].astype('int')

    X = df_vals.values
    y = df['target'].values

    return X, y, df


def buy_sell_hold(*args):
    cols = [c for c in args]
    requirement = 0.0004
    for col in cols:
        if col > requirement:
            return 1
        if col < -requirement:
            return -1
    return 0


        
        


if __name__ == '__main__':
    # Analysis of opening an order with sl definied and closing order at definied time
    
    #=================INPUT=====================
    X, y, df = extract_futuresets('M5', 'HKInd', '01:00', '04:45', dt.date(2022,1,1))
    
    X_train, X_test, y_train, y_test = train_test_split(X,
                                                        y,
                                                        test_size = 0.25)
    
    clf = VotingClassifier([('lsvc', svm.LinearSVC()),
                            ('knn', neighbors.KNeighborsClassifier()),
                            ('rfor', RandomForestClassifier())
                            ])
    
    clf.fit(X_train, y_train)
    confidence = clf.score(X_test, y_test)
    print('Accuracy:', confidence)
    predictions = clf.predict(X_test)
    print('Predicted spread:', Counter(predictions))

    filename = f'3_Analysis/HKInd_ML_model.pickle'

    with open(filename, 'wb') as f:
        pickle.dump(clf, f)
    print('File saved as:', filename)
    print()