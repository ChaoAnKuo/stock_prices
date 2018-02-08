import datetime, fire, sqlite3
import pandas as pd
from pandas_datareader import data as web

def update():
    conn = sqlite3.connect('NASDAQ.db')
    c = conn.cursor()

    c.execute('SELECT End FROM period')
    E = c.fetchone()
    end_date = datetime.datetime.strptime(E[0],'%Y-%m-%d')
    today = datetime.datetime.today()

    if (today-end_date).total_seconds() > 86400: # check updated today
        start_date = end_date+datetime.timedelta(days=1)
    
        c.execute('SELECT Symbol FROM companies')
        L = c.fetchall()
    
        stocks = []
        for i in range(len(L)):
            df = web.DataReader(L[i][0], 'iex', start_date, today)
            stocks.append(df)
    
        stocks = pd.concat(stocks, keys=L)
        stocks.reset_index(level=(0,1), inplace=True)
        stocks.rename(columns={'level_0': 'Symbol'}, inplace=True)
        
        c.execute('UPDATE period set End = ?', \
                 (today.strftime('%Y-%m-%d'),))
        stocks.to_sql('stocks', conn, if_exists='append', index=False)
        
        conn.commit()
    else:
        print('The database has been updated today.')

    conn.close()

# daily update
# =============================================================================
# from threading import Timer
# def daily_update(s=86400):
#     update()
#     t = Timer(s, daily_update, (s,))
#     t.start()
# =============================================================================
    
def main():
    fire.Fire(update)
    
if __name__ == '__main__':
    main()