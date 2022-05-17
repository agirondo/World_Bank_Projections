import pandas as pd
import time
import requests
from statsmodels.tsa.ar_model import AutoReg as AR

def get_data(i,countries): # retrieves dictionary with country as key and dataframe as value
    data={}
    for c in countries:
        try:
            
            time.sleep(1)
            r=requests.get(f'http://api.worldbank.org/v2/country/{c}/indicator/{i}?date=1970:2020&format=json').json()[1]
            df=pd.DataFrame(r)
            df=df[['date','value']].set_index('date')
            data[c]=df
        except:
            pass
    return data

def get_df(data):
    countries=data.keys()
    resultado=pd.DataFrame(columns=['country','error2019','error2020'])
    for z in countries:
        
        df=data[z].iloc[:2020]
        df=df.reindex(index=df.index[::-1])
        if df.isnull().values.any():
            continue
        else:
            train, test = df.value[:-2], df.value[-2:-1]
            modelo=AR(train, lags=5).fit()
            pred=modelo.predict(len(train)-1,len(train)-1)
            error2019=(test[0]-pred[0])/pred[0]

            train, test = df.value[:-1], df.value[-1:]
            modelo=AR(train, lags=5).fit()
            pred=modelo.predict(len(train)-1,len(train)-1)
            error2020=(test[0]-pred[0])/pred[0]

            resultado=resultado.append({'country':z,'error2019':error2019,'error2020':error2020},ignore_index=True)

    return resultado