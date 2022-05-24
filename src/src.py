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

def get_df(data,p,d,q,year):
    countries=data.keys()
    resultado=pd.DataFrame(columns=['country',f'error{year-5}_{year-1}',f'error{year}'])
    for z in countries:
        
        df=data[z].iloc[:year]
        df=df.reindex(index=df.index[::-1])
        if df.isnull().values.any():
            continue
        else:

            train, test = df.value[:-6], df.value[-6:-1]
            modelo=ARIMA(train, order=(p,d,q)).fit()
            pred=modelo.predict(len(train)-5,len(train)-1)
            pred.index=[f'{year-5}',f'{year-4}',f'{year-3}',f'{year-2}',f'{year-1}']
            error_before=(pred-test).abs().sum()/len(pred) 

            train, test = df.value[:-1], df.value[-1:]
            modelo=ARIMA(train, order=(p,d,q)).fit()
            pred=modelo.predict(len(train)-1,len(train)-1)
            error_target=test[0]-pred[0]


            resultado=resultado.append({'country':z,f'error{year-5}_{year-1}':error_before,f'error{year}':error_target},ignore_index=True)

    return resultado
