import  requests
from xml.sax import parseString
from bs4 import BeautifulSoup
import json
import re
import os
import csv
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


def get_stock_data(tickers):
    api_key = '28fc4e3838a1dd4a6a9cfa76630cdb7a'
    tickers_list = []
    tickers_string = ''

    for key,value in tickers:
        tickers_list.append(key) 
    
    tickers_list = tickers_list[0:10]
    

   

#works
   # for item in tickers_list:
    #    data = requests.get('https://api.marketstack.com/v1/eod?access_key='+api_key+'&symbols='+item+'&date_from=2013-01-01&date=2020-01-01&limit=1000')
    #    stock_data = json.loads(data.text)
    #    for dic in range(len(stock_data['data'])):
    #        print(stock_data['data'][dic]['symbol'] + ": "+stock_data['data'][dic]['date'] + ": " + str(stock_data['data'][dic]['close']))



    #print(stock_data)


    #data_2 = requests.get('https://api.marketstack.com/v1/eod?access_key='+api_key+'&symbols=AAPL&date_from=2013-01-01&date=2020-01-01&limit=1000&offset=1000')
    
    #stock_data_2 = json.loads(data_2.text)
    



    

    #for dic in range(len(stock_data_2['data'])):
       # print(stock_data_2['data'][dic]['date'] + ": " + str(stock_data_2['data'][dic]['close']))
    


    

    

    
  
    pass


def get_economic_data():
    key = 'e7cVuAp2R1gsCUf16GBz'

    cpi = requests.get('https://api.stlouisfed.org/fred/series/observations?series_id=CPILFESL&api_key=0826dcd62489d3c9b0e3a3d14dea492b&file_type=json&observation_start=2013-01-01')
    #real_gdp = requests.get('https://api.stlouisfed.org/fred/series/observations?series_id=GDPC1&api_key=0826dcd62489d3c9b0e3a3d14dea492b&file_type=json&observation_start=1990-01-01')

    cpi_data = json.loads(cpi.text)


    #real_data = json.loads(real_gdp.text)

    for dic in range(len(cpi_data['observations'])):
        print(cpi_data['observations'][dic]['date'] + ": " + cpi_data['observations'][dic]['value'])
        #print(real_data['observations'][dic]['date'] + ": " + real_data['observations'][dic]['value'])
       
    

    
   
    pass
    #get average prices of top 100 stocks and compare that to gdp....do they go at the same rate?
    #^^ could do the same with CPI or GDP deflator... calculate if stocks increase/decrease at the same rate as inflation





   # 0826dcd62489d3c9b0e3a3d14dea492b



if __name__ == '__main__':

    tickers = get_spy_data('https://stockmarketmba.com/stocksinthesp500.php')
    get_stock_data(tickers)
    get_economic_data()
    





    unittest.main(verbosity=2)