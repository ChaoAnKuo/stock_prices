import datetime, fire, sqlite3
import pandas as pd

def stock_price(symbol='', start_date='2017-01-01', end_date = 'today'):
    if end_date == 'today':
        end_date = datetime.date.today().strftime('%Y-%m-%d')
    
    pd.set_option('display.max_rows', None) # display all rows
    
    conn = sqlite3.connect('NASDAQ.db')
    c = conn.cursor()
    
    if symbol == '': # return the list of available symbols
        c.execute('SELECT Symbol, Name FROM companies')
        L = c.fetchall()
        L = pd.DataFrame(L, columns=('Symbol', 'Name'))
        print(L)
    else:
        c.execute('SELECT date, open, close, low, high, volume ' + \
                  'FROM stocks WHERE Symbol=? AND date BETWEEN ? and ?' \
                  , (symbol, start_date, end_date))
        D = c.fetchall()
        D = pd.DataFrame(D, \
                         columns=('Date','Open','Close','Min','Max','Volume'))
        D.set_index('Date', inplace=True)
        
        D['PNL'] = MACD(D['Close'], spans=[12,26,9]) # compute PNL
        print(D)
    
    c.close()
    
def MACD(data, spans=[12,26,9]):
    S = data.ewm(span=spans[0]).mean() # short-term exponential average
    L = data.ewm(span=spans[1]).mean() # long-term exponential average
    MACD = S-L
    Signal = MACD.ewm(span=spans[2]).mean() # signal line
    
    PNL, Hold = [0], 0
    for i in range(1, MACD.shape[0]):
        PNL.append(PNL[-1]+Hold*(data[i]-data[i-1]))
        if MACD[i-1] <= Signal[i-1] and MACD[i] > Signal[i]:
            Hold += 1
        elif MACD[i-1] >= Signal[i-1] and MACD[i] < Signal[i]:
            Hold -= 1
    
    return PNL

def main():
    fire.Fire(stock_price)

if __name__ == '__main__':
    main()