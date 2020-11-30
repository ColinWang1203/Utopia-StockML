# conda install -c conda-forge fbprophet
# conda install plotly -y 
import pandas as pd
from fbprophet import Prophet

# day predict example YYYY-MM-DD or YYYYMMDD both ok
list1 = [('20191201',123),('20191202',124),('20191203',125)]
# pd.DataFrame(data=list1, index=None, columns=None, dtype=None, copy=False)
df1 = pd.DataFrame(data=list1, columns=['ds','y'])
print(df1)
m = Prophet()
m.fit(df1)
future = m.make_future_dataframe(periods=3, freq = "D")
forecast = m.predict(future)
print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']])

# month predict example 
# note that 2019-10 will not be generated, but the None will be predicted
list1 = [('2019-8',121),('2019-9',122),('2019-11',None),('2019-12',125)]
# pd.DataFrame(data=list1, index=None, columns=None, dtype=None, copy=False)
df1 = pd.DataFrame(data=list1, columns=['ds','y'])
print(df1)
m = Prophet()
m.fit(df1)
future = m.make_future_dataframe(periods=3, freq = "MS") # M will give odd result, use first day of month : MS
forecast = m.predict(future)
print(type(forecast))
print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]) # note these are default label, use them to get item
print(forecast['yhat'].iloc[-1]) # note that the yhat are all predicted, number will not be the same as assign
'''
# try the official website example
df = pd.read_csv('Test_prophet.csv')
# get rows 2905
print(df.tail())
print(df.shape)
print(type(df))
# Init
m = Prophet()
m.fit(df)
future = m.make_future_dataframe(periods=365)
#now future has rows 2905 + 365 = 3270
print(future.tail())
print(future.shape)
# Predict
forecast = m.predict(future)
print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())
# Plot
fig1 = m.plot(forecast)
print(type(fig1))
fig1.show()
fig1.waitforbuttonpress(0)
fig2 = m.plot_components(forecast)
fig2.show()
fig2.waitforbuttonpress(0)
'''

