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

def get_economic_data():
    key = 'e7cVuAp2R1gsCUf16GBz'


    output_dict = {}

    cpi = requests.get('https://api.stlouisfed.org/fred/series/observations?series_id=CPILFESL&api_key=0826dcd62489d3c9b0e3a3d14dea492b&file_type=json&observation_start=2013-01-01')
    #real_gdp = requests.get('https://api.stlouisfed.org/fred/series/observations?series_id=GDPC1&api_key=0826dcd62489d3c9b0e3a3d14dea492b&file_type=json&observation_start=1990-01-01')

    cpi_data = json.loads(cpi.text)


    #real_data = json.loads(real_gdp.text)

    for dic in range(len(cpi_data['observations'])):

        date = cpi_data['observations'][dic]['date']
        value = cpi_data['observations'][dic]['value']

        output_dict[date] = value
        
        #print(real_data['observations'][dic]['date'] + ": " + real_data['observations'][dic]['value'])
       
    
    #print(len(output_dict))
    return(output_dict)
    
   
    pass
    #get average prices of top 100 stocks and compare that to gdp....do they go at the same rate?
    #^^ could do the same with CPI or GDP deflator... calculate if stocks increase/decrease at the same rate as inflation





   # 0826dcd62489d3c9b0e3a3d14dea492b


def get_stock_data(tickers,dates):
    api_key = '28fc4e3838a1dd4a6a9cfa76630cdb7a'
    tickers_list = []
    temp_dict = {}

    date_close_list = []
    
    final_dict = {}

    for key,value in tickers:
        tickers_list.append(key) 
    
    tickers_list = tickers_list[0:100]
    

   

#works
   # for item in tickers_list:
    data = requests.get('https://api.marketstack.com/v1/eod?access_key='+api_key+'&symbols=AAPL,MFST&date_from=2013-01-01&date=2020-01-01&limit=1000')
    stock_data = json.loads(data.text)

    for dic in range(len(stock_data['data'])):

         #find just the date, not the time

        date = (re.search("(\d\d\d\d-\d\d-\d\d)", stock_data['data'][dic]['date'])).group()
       
       #might not need if statement below
        #if date in dates:

        temp_dict['date']  = date

        

       
        temp_dict['close'] =  stock_data['data'][dic]['close']

        date_close_list.append(temp_dict)

        temp_dict = {}

    

    
    final_dict[stock_data['data'][dic]['symbol']] = date_close_list

        

        #print(stock_data['data'][dic]['symbol'] + ": "+stock_data['data'][dic]['date'] + ": " + str(stock_data['data'][dic]['close']))
    return(final_dict)


    #print(stock_data)


    #data_2 = requests.get('https://api.marketstack.com/v1/eod?access_key='+api_key+'&symbols=AAPL&date_from=2013-01-01&date=2020-01-01&limit=1000&offset=1000')
    
    #stock_data_2 = json.loads(data_2.text)
    



    

    #for dic in range(len(stock_data_2['data'])):
       # print(stock_data_2['data'][dic]['date'] + ": " + str(stock_data_2['data'][dic]['close']))
    


    

    

    
  
    pass



def create_stock_tables(stock_dict, db_filename):
    
    con = sqlite3.connect(db_filename)
    cur = con.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS Stock_Close_Prices (id INTEGER PRIMARY KEY, ticker TEXT)")

    i = 1
    
    
    for ticker_symbol,values in stock_dict.items():

       
        
        cur.execute("INSERT OR IGNORE INTO Stock_Close_Prices (id,ticker) VALUES (?,?)", (i,ticker_symbol))
        i += 1
        
    con.commit()



    pass


def drop_table(db_filename):
    con = sqlite3.connect(db_filename)
    cur = con.cursor()

    cur.execute("DROP TABLE Stock_Close_Prices")
    con.commit()

if __name__ == '__main__':

    tickers = get_spy_data('https://stockmarketmba.com/stocksinthesp500.php')
    data = get_stock_data(tickers,get_economic_data())

    #drop_table('final_project.db')

    create_stock_tables(data,'final_project.db')



    
    





    unittest.main(verbosity=2)