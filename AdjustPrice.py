#!/usr/bin/env python
# coding: utf-8

# In[461]:


import numpy as np
import pandas as pd
import pytse_client as tse
import jdatetime
from datetime import datetime

from scipy.ndimage.interpolation import shift


# # get data from the web

# In[462]:


#tickers = tse.download(symbols="all", write_to_csv=True,  include_jdate=True)
Price1 = pd.read_csv("/home/khaled/Project/AdjustedPrice_P/tickers_data/قشکر.csv")
Price = Price1[Price1['volume']>100].copy()


# ## We want to adjust the price from the 1400-01-01 till the 1401-12-01 with respect to all capital injections that occurred in this interval

# In[463]:


FirstDayOfInterval = '1398-01-01'
LastDayOfInterval = '1401-12-01'

gregorian_date = jdatetime.date(int(LastDayOfInterval[0:4]),
                                int(LastDayOfInterval[5:7]),int(LastDayOfInterval[8:10])).togregorian()
Fgregorian_date = jdatetime.date(int(FirstDayOfInterval[0:4]),
                                 int(FirstDayOfInterval[5:7]),int(FirstDayOfInterval[8:10])).togregorian()

def DateT(a):
    return(datetime.fromisoformat((a)))
Price['date'] = Price['date'].apply(lambda x: DateT(x))
PriceFilter = Price[(Price['date'] > pd.Timestamp(pd.to_datetime(Fgregorian_date))) & (Price['date'] < pd.Timestamp(pd.to_datetime(gregorian_date)))]


# In[464]:


PriceFilter.iloc[-1, Loc]


# In[465]:


Prod


# In[466]:


Ratio =  PriceFilter['adjClose']/ PriceFilter['yesterday']
CumProd = Ratio.cumprod()
Prod = Ratio.prod()
AdjusetCumProd = CumProd/Prod
Loc = PriceFilter.columns.get_loc('adjClose')
a = PriceFilter.iloc[-1, Loc]*AdjusetCumProd
PriceFilter.insert(Loc+1,"AdjustedPrice", a, True)
PriceFilter


# In[468]:


import plotly.express as px 
import plotly.graph_objects as go
from plotly.subplots import make_subplots
fig = go.Figure()
fig.add_trace(go.Scatter(x=PriceFilter['date'], y=PriceFilter['adjClose'],name="BeforAdjust"))
fig.add_trace(go.Scatter(x=PriceFilter['date'], y=PriceFilter['AdjustedPrice'], name="AfterAdjust"))


# In[ ]:





# In[ ]:




