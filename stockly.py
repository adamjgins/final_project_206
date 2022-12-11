import  requests
from xml.sax import parseString
from bs4 import BeautifulSoup
import json
import re
import csv
import matplotlib.pyplot as plt
import os
import sqlite3
import unittest
import unittest
from datetime import datetime

def organize_by_year_month(data):
  # Create a dictionary to hold the organized data
  organized_data = {}
  
  # Loop through each dictionary in the list
  for datapoint in data:
    # Parse the date string into a datetime object
    
    date = datetime.strptime(datapoint['date'], '%Y-%m-%d')
  

    
    # Get the year and month from the datetime object
    year = date.year
    month = date.month
    
    # Add the year and month to the dictionary as keys, if they don't already exist
    if year not in organized_data:
      organized_data[year] = {}
    if month not in organized_data[year]:
      organized_data[year][month] = []
      

    organized_data[year][month].append(datapoint)


    
  
  # Return the organized data



  
  return organized_data





def get_spy_data(link):

    tickers_dic ={}

    
    page = requests.get(link)

    soup = BeautifulSoup(page.content, "html.parser")

    rows = soup.find_all("tr")

    

 

    for row in rows[1:]:

        columns = row.find_all("td",None)

        ticker_link = columns[0]

        marketcap = columns[5]

        ticker = ticker_link.find("a",None)


        if ticker != None:

            marketcap = int(marketcap.text.replace(',','').strip('$'))
            ticker = ticker.text

            tickers_dic[ticker] = marketcap

            tickers_dic_sorted = sorted(tickers_dic.items(), key=lambda x:x[1], reverse=True)




    return(tickers_dic_sorted)

    




    pass

def make_list_of_dictionaries(dict):
    
    final_list = []
 

    point = ''

    if 'observations' in dict:
        point = 'observations'

    if 'priceData' in dict:
        point = 'priceData'

    if 'data' in dict:
        point = 'data'
   
    for dic in range(len(dict[point])):
            temp_dict = {}

         #find just the date, not the time

            date = (re.search("(\d\d\d\d-\d\d-\d\d)", dict[point][dic]['date'])).group()
       
       #might not need if statement below
        #if date in dates:

            temp_dict['date']  = date

        
            if 'ticker' in dict:
                temp_dict['ticker'] = dict['ticker']

            if 'symbol' in dict[point][dic]:
                temp_dict['ticker'] = dict[point][dic]['symbol']
            
            if 'close' in dict[point][dic]:

                temp_dict['close'] =  dict[point][dic]['close']

            if 'volume' in dict[point][dic]:


                temp_dict['volume'] =  dict[point][dic]['volume']

            if 'value' in dict[point][dic]:
                temp_dict['value'] =  dict[point][dic]['value']

       

            final_list.append(temp_dict)

            

    final = organize_by_year_month(final_list)

    
    return(final)


        

def get_economic_data():
    key = 'e7cVuAp2R1gsCUf16GBz'


    output_dict = {}

    cpi = requests.get('https://api.stlouisfed.org/fred/series/observations?series_id=CPILFESL&api_key=0826dcd62489d3c9b0e3a3d14dea492b&file_type=json&observation_start=2013-01-01')
    #real_gdp = requests.get('https://api.stlouisfed.org/fred/series/observations?series_id=GDPC1&api_key=0826dcd62489d3c9b0e3a3d14dea492b&file_type=json&observation_start=1990-01-01')

    cpi_data = json.loads(cpi.text)


    #real_data = json.loads(real_gdp.text)


    

    output_dict =  make_list_of_dictionaries(cpi_data)
    


    #for dic in range(len(cpi_data['observations'])):

     #   date = cpi_data['observations'][dic]['date']
      #  value = cpi_data['observations'][dic]['value']

       # output_dict[date] = value
        
        #print(real_data['observations'][dic]['date'] + ": " + real_data['observations'][dic]['value'])
       
    
    #print(len(output_dict))



    return(output_dict)
    
   
    pass
    #get average prices of top 100 stocks and compare that to gdp....do they go at the same rate?
    #^^ could do the same with CPI or GDP deflator... calculate if stocks increase/decrease at the same rate as inflation





   # 0826dcd62489d3c9b0e3a3d14dea492b




def get_crypto_data():
    temp_dict = {}
    

    api_key = 'd8e0dd9b278c792c5bf7256c7e249ed4569f700c'

    headers = {
    'Content-Type': 'application/json'
}
    requestResponse = requests.get("https://api.tiingo.com/tiingo/crypto/prices?tickers=btcusd&startDate=2013-01-01&resampleFreq=1day&token="+api_key, headers=headers)
    

    crypto_data = json.loads(requestResponse.text)

    crypto_data = crypto_data[0]

    organized_dict = make_list_of_dictionaries(crypto_data)
   
    

    for year,d in organized_dict.items():
        for month,close in d.items():
            
            organized_dict[year][month] = find_average_of_list(close)


    
   
    organized_dict = dict(sorted(organized_dict.items(), key=lambda x: x[0], reverse=True))

    for year,months in organized_dict.items():
        organized_dict[year] = dict(sorted(months.items(), key=lambda x: x[0], reverse=True))
    

    return(organized_dict)



def get_stock_data(tickers):

    print('runnning get stock data')
    api_key = '28fc4e3838a1dd4a6a9cfa76630cdb7a'
    tickers_list = []
    temp_dict = {}

   
    

    organized_list = []
    
    final_dict = {}

    

    for key,value in tickers:
        tickers_list.append(key) 
    
    ticker = tickers_list[0]

   
    

   

#works
    #original for loop for multplie stocks
    #for item in tickers_list:

    data = requests.get('https://api.marketstack.com/v1/eod?access_key='+api_key+'&symbols='+ticker+'&date_from=2013-01-01&date=2020-01-01&limit=1000')
    stock_data = json.loads(data.text)


    data_2 = requests.get('https://api.marketstack.com/v1/eod?access_key='+api_key+'&symbols='+ticker+'&date_from=2013-01-01&date=2020-01-01&limit=1000&offset=1000')
    
    stock_data_2 = json.loads(data_2.text)

    data_3 = requests.get('https://api.marketstack.com/v1/eod?access_key='+api_key+'&symbols='+ticker+'&date_from=2013-01-01&date=2020-01-01&limit=1000&offset=2000')
    
    stock_data_3 = json.loads(data_3.text)

    for dic in range(len(stock_data_2['data'])):
        stock_data['data'].append(stock_data_2['data'][dic])

    for dic in range(len(stock_data_3['data'])):
        stock_data['data'].append(stock_data_3['data'][dic])

    


  
    #print(stock_data['data'])

    



    

    #for dic in range(len(stock_data_2['data'])):
       # print(stock_data_2['data'][dic]['date'] + ": " + str(stock_data_2['data'][dic]['close']))
    

    organized_list = make_list_of_dictionaries(stock_data)
   



    

    for year,d in organized_list.items():
        for month,close in d.items():
            
            organized_list[year][month] = find_average_of_list(close)


 
    
    
    return(organized_list)
    

    

    
  
pass


def find_average_of_list(list):

    total_close = 0
    total_volume = 0
    divisor = len(list)

    output_dict = {}

    for item in list:
        total_close += item['close']
        total_volume += item['volume']

    
    total_close = total_close/divisor
    total_volume = total_volume/divisor

    output_dict['ticker'] = item['ticker']


    output_dict['avg_close'] = round(total_close,2)
    output_dict['avg_vol'] = round(total_volume,2)


    return(output_dict)  





def create_dates_table(stock_dict, db_filename):
    
    con = sqlite3.connect(db_filename)
    cur = con.cursor()

    month_dict = {	1:'Janauary',
		2:'February',
		3:'March',
		4:'April',
		5:'May',
		6:'June',
		7:'July',
		8:'August',
		9:'September',
		10:'October',
		11:'November',
		12:'December'		}

    cur.execute("CREATE TABLE IF NOT EXISTS dates (id INTEGER PRIMARY KEY, date TEXT UNIQUE)")

    for year,data in stock_dict.items():
        for month,close in data.items():
            date = (str(month_dict[month])+", " + str(year))
            cur.execute("INSERT OR IGNORE INTO dates(date) VALUES (?)", [date])

    




    
    #i = 1
    
    
    #for ticker_symbol,values in stock_dict.items():

     #   print(ticker_symbol)

       
        
      #  cur.execute("INSERT OR IGNORE INTO Stock_Close_Prices (id,ticker) VALUES (?,?)", (i,ticker_symbol))
       # i += 1
        
    con.commit()



    pass


def create_stock_table(stock_dict,db_filename):

    con = sqlite3.connect(db_filename)
    cur = con.cursor()


    



    cur.execute("CREATE TABLE IF NOT EXISTS stock_info (id INTEGER PRIMARY KEY, ticker TEXT, avg_close DOUBLE, avg_vol DOUBLE)")


    cur.execute("SELECT id FROM stock_info WHERE id = (SELECT MAX(id) FROM stock_info)")
    start = cur.fetchone()
    
    if (start != None):
        start = start[0]+1
    else:
        start = 1

   
    
    
    

    i = 1

    for year,data in stock_dict.items():
        for month,close in data.items():
            if (i >= start and i< (start+25)):
                cur.execute("INSERT OR IGNORE INTO stock_info(ticker,avg_close,avg_vol) VALUES (?,?,?)", (close['ticker'],close['avg_close'],close['avg_vol']))
            i +=1
                
    con.commit()

def create_crypto_table(crypto_dict,db_filename):

    con = sqlite3.connect(db_filename)
    cur = con.cursor()

    

    

    cur.execute("CREATE TABLE IF NOT EXISTS crypto_info (id INTEGER PRIMARY KEY, ticker TEXT, avg_close DOUBLE, avg_vol DOUBLE)")
    
    cur.execute("SELECT id FROM crypto_info WHERE id = (SELECT MAX(id) FROM crypto_info)")
    start = cur.fetchone()
    
    if (start != None):
        start = start[0]+1
    else:
        start = 1


    i = 1

    

    for year,data in crypto_dict.items():
        for month,close in data.items():
            if (i >= start and i< (start+25)):
               
                cur.execute("INSERT OR IGNORE INTO crypto_info(ticker,avg_close,avg_vol) VALUES (?,?,?)", (close['ticker'],close['avg_close'],close['avg_vol']))
            i +=1
    con.commit()







def drop_table(db_filename):
    con = sqlite3.connect(db_filename)
    cur = con.cursor()

    cur.execute("DROP TABLE dates")
    cur.execute("DROP TABLE stock_info")
    cur.execute("DROP TABLE crypto_info")
    con.commit()

if __name__ == '__main__':

    val = 1


    if val == 1:
        tickers = get_spy_data('https://stockmarketmba.com/stocksinthesp500.php')
        economic_data = get_economic_data()
        crypto_data = get_crypto_data()
        stock_data = get_stock_data(tickers)

    

        create_dates_table(stock_data,'final_project.db')
        create_stock_table(stock_data,'final_project.db')
        create_crypto_table(crypto_data,'final_project.db')

    else:
        drop_table('final_project.db')




    
    





    unittest.main(verbosity=2)