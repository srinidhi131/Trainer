
import os
import pandas as pd
from pathlib import Path
from typing import List
import yfinance as yf
import sys

class DataFetcher():
    
    def __init__(self,
                 stock_symbols: List[str],
                 start_date: str ,
                 end_date: str ,
                 directory_path: str = "rl\data",
                 ) -> None:
        
        Path(directory_path).mkdir(parents=True, exist_ok=True)
        
        self.stock_symbols = stock_symbols
        self.start_date = start_date
        self.end_date = end_date
        self.directory_path = directory_path
        
    def fetch_and_merge_data(self) -> None:
        
        final_df = None
        
        for stock in self.stock_symbols:
            
            file_path = os.path.join(self.directory_path, "{}.csv".format(stock))
            if not os.path.exists(file_path):
                data = yf.download(stock, start=self.start_date, end=self.end_date)
                if data.size > 0:
                    data.to_csv(file_path)
                    file = open(file_path).readlines()
                    if len(file) < 10:
                        os.remove(file_path)
            
            if os.path.exists(file_path):
                df = pd.read_csv(file_path)
                stock_name = file_path.split('\\')[2].split('.')[0]
                df['Name'] = stock_name

                if final_df is None:
                    final_df = df
                else:
                    final_df = final_df.append(df, ignore_index=True)
                
                os.remove(file_path)
                
        path = os.path.join(self.directory_path, 'stocks.csv')
        final_df.to_csv(path, index=False)
    
class Preprocessor():
    
    def __init__(self,
                 df_directory: str = 'rl\data',
                 file_name: str = 'stock.csv',
                 ) -> None:
            
        self.df_directory = df_directory
        path = os.path.join(df_directory, file_name)
        self.df = pd.read_csv(path) 
        
    def collect_close_prices(self) -> pd.DataFrame:
        
        self.df['Date'] = pd.to_datetime(self.df['Date'])
        dates = pd.date_range(self.df['Date'].min(), self.df['Date'].max())
        stocks = self.df['Name'].unique()
        close_prices = pd.DataFrame(index=dates)

        for stock in stocks:
            df_temp = self.df[self.df['Name'] == stock]
            df_temp2 = pd.DataFrame(data=df_temp['Close'].to_numpy(), index=df_temp['Date'], columns=[stock])
            close_prices = pd.concat([close_prices, df_temp2], axis=1)  
        self.df = close_prices
        return close_prices
        
    def handle_missing_values(self) -> pd.DataFrame:
        
        self.df.dropna(axis=0, how='all', inplace=True)
        self.df.fillna(method='ffill', inplace=True)
        self.df.fillna(method='bfill', inplace=True)
        self.df.to_csv(os.path.join(self.df_directory, 'close.csv'))
        return self.df   
  
    
def load_data(initial_date: str, 
              final_date: str, 
              tickers_subset: str,
              read: True,
              mode: str = 'test') -> pd.DataFrame:
    stocks_symbols=['AAPL','TSLA','MSFT','VZ','AMZN','BA','MS','DB','JPM','META','INTC','GS','HPE','TCS','WMT','T','TGT','WFC','V']

    if not read:
        if os.path.exists("rl\data\\stocks.csv"):
            os.remove("rl\data\\stocks.csv")
        if os.path.exists("rl\data\\close.csv"):
            os.remove("rl\data\\close.csv")
        r=DataFetcher(stocks_symbols,
                 initial_date,
                 final_date,
                 "rl\data")
        r.fetch_and_merge_data()
        p= Preprocessor(df_directory='rl\data',file_name='stocks.csv')
    
        d = p.collect_close_prices()
        d = p.handle_missing_values()
        return "data downloaded"
    else:
        print('\n>>>>> Reading the data <<<<<',file=sys.stdout)
        
        df = pd.read_csv('rl\data\\close.csv', index_col=0)
        with open(tickers_subset) as f:
            stocks_subset = f.read().splitlines()
            stocks_subset = [ticker for ticker in stocks_subset if ticker in df.columns]
            
        df = df[stocks_subset]
    
    time_horizon = df.shape[0]
    
    if mode == 'train':
        df = df.iloc[:3*time_horizon//4, :]
    else:
        df = df.iloc[3*time_horizon//4:, :]
        
    return df
