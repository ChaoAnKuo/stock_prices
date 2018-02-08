import datetime, fire, sqlite3
import pandas as pd
from pandas_datareader import data as web
from urllib.request import urlopen

def construct_database(start_date='2017-01-01', end_date='today'):
    '''
    Construct a database for stock prices.
    
    start_date : String 
        The first date of the database (e.g., '2017-01-01').
    end_date   : String
        The last date of the database (e.g., '2017-12-31' or 'today').
    '''
    
    start_date = datetime.datetime.strptime(start_date,'%Y-%m-%d')
    if end_date == 'today':
        end_date = datetime.datetime.today()
    else:
        end_date = datetime.datetime.strptime(end_date,'%Y-%m-%d')
    
    period = [[start_date.strftime('%Y-%m-%d'), \
                 end_date.strftime('%Y-%m-%d')]]
    period = pd.DataFrame(data=period, columns=['Start','End'])
    
    # Collect company list from NASDAQ
    url = 'https://www.nasdaq.com/screening/' + \
        'companies-by-industry.aspx?exchange=NASDAQ&render=download'
    csv = urlopen(url)
    companies = pd.read_csv(csv)
    companies = companies.head(10) # use the first 10 companies as an example
    
    # Collect stock price data from Investors Exchange
    stocks = []
    for i in range(companies.shape[0]):
        df = web.DataReader(companies.get_value(i,'Symbol'), 'iex', \
                            start_date, end_date)
        stocks.append(df)

    stocks = pd.concat(stocks, keys=companies['Symbol'])
    stocks.reset_index(level=(0,1), inplace=True)
    
    # Store data in a SQL database
    conn = sqlite3.connect('NASDAQ.db')
    
    period.to_sql('period', conn, if_exists='replace', index=False)
    companies.to_sql('companies', conn, if_exists='replace', index=False)
    stocks.to_sql('stocks', conn, if_exists='replace', index=False)

    conn.commit()
    conn.close()
    print('The database is successfully constructed.')
    
def main():
    fire.Fire(construct_database)

if __name__ == '__main__':
    main()