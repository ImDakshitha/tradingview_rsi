# Tradingview RSI is based on Relative Moving Average. In Tradingview Relative Moving Average aka `ta.rma` defined as,

#      pine_rma(src, length) =>
#          alpha = 1/length
#          sum = 0.0
#          sum := na(sum[1]) ? ta.sma(src, length) : alpha * src + (1 - alpha) * nz(sum[1])

# note that when calculating sum for the first value of the given dataset,the previous value becomes NaN because there are no data available beyond that. So the ta.rma function calculates Simple Moving Average only for that instance, but from second data point onwords there is a value available at `sum[1]` position.

# So make sure to provide at least 100 dataponints to get a RSI value too close to the value given in Tradingview.

   
    import numpy as np
    import pandas as pd
    from pandas import DataFrame, Series
    from pandas import DataFrame, Series, isna
   
    #tradingview ta.rma function

    def rma(dataframe: DataFrame, length: int = 14):
        alpha = 1.0 / length
        series = dataframe['close']
        for i in range(1, series.size):
            if not isna(series[i - 1]):
                 series.iloc[i] = (series[i] * alpha) + (1 - alpha) * (series[i - 1])  
            else: 
                series.iloc[i]=(series[i]/length)
        return series
    
    #tradingview ta.sma function

    def sma(dataframe: DataFrame, length: int = 14):
        series = dataframe['close']
        sum=0
        for i in range(1, series.size):
            sum = sum+(series.iloc[i]/length) 
        return sum  
    
    
    #tradingview ta.rsi function
    def rsi_tradingview(ohlc: pd.DataFrame, period: int = 14, round_rsi: bool = False):
        delta =ohlc['close'].diff()
        delta=delta.fillna(0)
        
        up = delta.copy()
        up[up < 0] = 0
        up1=pd.DataFrame(up)
        up2=pd.Series(rma(up1,14))
        down = delta.copy()
        down[down > 0] = 0
        down *= -1
        down1=pd.DataFrame(down)
        down2=pd.Series(rma(down1,14))
    
        rsi = np.where(up2 == 0, 0, np.where(down2 == 0, 100, 100 - (100 / (1 + (up2 / down2)))))
        return np.round(rsi, 2) if round_rsi else rsi

