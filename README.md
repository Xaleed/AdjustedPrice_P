
## Table of contents
* [Price Adjustment](#Price-Adjustment)
* [Description](#Description)

## Price Adjustment
 An important issue in the Iranian stock market is the adjustment of stock prices after the capital injection. In this work, we want to calculate the adjusted price of a stock in any arbitrary interval with respect to the end of the interval. Consider the following two vector
 ```math
 P = (P_1,P_2,\cdots,P_n) \\
 P^{y} = (P_1^{y},P_2^{y},\cdots,P_n^{y}).
 ```
 Where $P_i$ is the price of stock  for the ($i$)th day and $P_i^{y}$ is the price of stock  for the ($i-1$)th day such that the adjustment on this price is calculated based on information of $i$th day. Now we can calculate the adjusted price with respect to all capital injections till the end of the interval using the following formula
 ```math
 P_i^{Adj}=P_n\prod_{k=i+1}^{n}\frac{P_i^{y}}{P_i}
 ```
## Description
This code is created of the following steps:
* calling Tehran stock exchange data from the web using package [pytse-client](https://pypi.org/project/pytse-client/) ...
```python
import numpy as np
import pandas as pd
import pytse_client as tse
tickers = tse.download(symbols="all", write_to_csv=True,  include_jdate=True)
Price = tickers["قشکر"]
```

* We want to adjust the price from the 1400-01-01 till the 1401-12-01 with respect to all capital injections that occurred in this interval.
```python
import jdatetime
from datetime import datetime
FirstDayOfInterval = '1396-01-01'
LastDayOfInterval = '1401-12-01'

gregorian_date = jdatetime.date(int(LastDayOfInterval[0:4]),
                                int(LastDayOfInterval[5:7]),int(LastDayOfInterval[8:10])).togregorian()
Fgregorian_date = jdatetime.date(int(FirstDayOfInterval[0:4]),
                                 int(FirstDayOfInterval[5:7]),int(FirstDayOfInterval[8:10])).togregorian()

def DateT(a):
    return(datetime.fromisoformat((a)))
Price['date'] = Price['date'].apply(lambda x: DateT(x))
PriceFilter = Price[(Price['date'] > pd.Timestamp(pd.to_datetime(Fgregorian_date))) & (Price['date'] < pd.Timestamp(pd.to_datetime(gregorian_date)))]
```
* And finally, by the following code, we can adjust the close prices
```python
Ratio =  PriceFilter['adjClose']/ PriceFilter['yesterday']
CumProd = Ratio.cumprod()
Prod = Ratio.prod()
AdjusetCumProd = CumProd/Prod
Loc = PriceFilter.columns.get_loc('adjClose')
a = PriceFilter.iloc[-1, Loc]*AdjusetCumProd
PriceFilter.insert(Loc+1,"AdjustedPrice", a, True)
PriceFilter

```
```python
import plotly.express as px 
import plotly.graph_objects as go
from plotly.subplots import make_subplots
fig = go.Figure()
fig.add_trace(go.Scatter(x=PriceFilter['date'], y=PriceFilter['adjClose'],name="BeforAdjust"))
fig.add_trace(go.Scatter(x=PriceFilter['date'], y=PriceFilter['AdjustedPrice'], name="AfterAdjust"))
```
![image info](./newplot.png)
	