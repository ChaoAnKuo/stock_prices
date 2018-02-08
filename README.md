Please try the following lines of code in the command prompt.
- Construct a database (NASDAQ.db) of stock prices from the start date to the end date.

  python construct_database.py --start_date '2017-01-01' --end_date '2017-12-31'
  
- Return the list of available symbols. 
  
  python stock_price.py
  
- Returns the historical price data and the PNL of a stock.
  
  python stock_price.py --symbol 'PIH' --start_date '2017-01-01' --end_date '2017-01-31'
  
- Update the database to today.
  
  python update.py

- Update the database every 30 seconds.
  
  python daily_update.py --s 30

In addition, to compute PNL, I adopt the MACD(12, 26, 9) trading strategy: 
1. Compute 12-day exponential moving average of the closing price.
2. Compute 26-day exponential moving average of the closing price.
3. Compute MACD (12-day EMA minus 26-day EMA).
4. Compute Signal (9-day EMA of the MACD).
5. Buy one share when the MACD turns up and crosses above the signal.
6. Sell one share when the MACD turns down and crosses below the signal.
