import pandas as pd
import time
import requests
from statsmodels.tsa.arima.model import ARIMA

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

def get_df(data,p=1,d=0,q=1):
    countries=data.keys()
    resultado=pd.DataFrame(columns=['country','error2015_2019','error2020'])
    for z in countries:
        
        df=data[z].iloc[:2020]
        df=df.reindex(index=df.index[::-1])
        if df.isnull().values.any():
            continue
        else:
            '''train, test = df.value[:-2], df.value[-2:-1]
            modelo=ARIMA(train,order=(p,d,q)).fit()
            pred=modelo.predict(len(train)-1,len(train)-1)
            error2019=test[0]-pred[0]'''

            train, test = df.value[:-6], df.value[-6:-1]
            modelo=ARIMA(train, order=(p,d,q)).fit()
            pred=modelo.predict(len(train)-5,len(train)-1)
            pred.index=['2015','2016','2017','2018','2019']
            error2015_2019=(pred-test).abs().sum()/len(pred) 

            train, test = df.value[:-1], df.value[-1:]
            modelo=ARIMA(train, order=(p,d,q)).fit()
            pred=modelo.predict(len(train)-1,len(train)-1)
            error2020=test[0]-pred[0]


            resultado=resultado.append({'country':z,'error2015_2019':error2015_2019,'error2020':error2020},ignore_index=True)

    return resultado
