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


def get_crypto_data():
    temp_dict = {}
    date_close_list = []

    api_key = 'd8e0dd9b278c792c5bf7256c7e249ed4569f700c'

    headers = {
    'Content-Type': 'application/json'
}
    requestResponse = requests.get("https://api.tiingo.com/tiingo/crypto/prices?tickers=btcusd&startDate=2019-01-02&resampleFreq=1day&token="+api_key, headers=headers)
    

    crypto_data = json.loads(requestResponse.text)

    crypto_data = crypto_data[0]


    for dic in range(len(crypto_data['priceData'])):

         #find just the date, not the time

            date = (re.search("(\d\d\d\d-\d\d-\d\d)", crypto_data['priceData'][dic]['date'])).group()
       
       #might not need if statement below
        #if date in dates:

            temp_dict['date']  = date

        

       
            temp_dict['close'] =  crypto_data['priceData'][dic]['close']

            temp_dict['volume'] =  crypto_data['priceData'][dic]['volume']
       

            date_close_list.append(temp_dict)

            temp_dict = {}


    
        

    date_close_list =  organize_by_year_month(date_close_list)



    

    for year,d in date_close_list.items():
        for month,close in d.items():
            
            date_close_list[year][month] = find_average_of_list(close)


 
    print(date_close_list)
    
    return(date_close_list)



def get_stock_data(tickers,dates):

    print('runnning get stock data')
    api_key = '28fc4e3838a1dd4a6a9cfa76630cdb7a'
    tickers_list = []
    temp_dict = {}

   
    

    date_close_list = []
    
    final_dict = {}

    

    for key,value in tickers:
        tickers_list.append(key) 
    
    tickers_list = tickers_list[0:100]

    #take this out when ready
    tickers_list = ['AAPL']
    

   

#works
    for item in tickers_list:

         #month Lists
        jan_list = []
        feb_list = []
        mar_list = []
        apr_list = []
        may_list = []
        jun_list = []
        jul_list = []
        aug_list = []
        sept_list = []
        oct_list = []
        nov_list = []
        dec_list = []

        months_dict = {}


        #year_list
        first_list = []
        second_list = []
        third_list = []
        fourth_list = []
        fifth_list = []
        six_list = []
        seventh_list = []
        eighth_list = []
        ninth_list = []
        tenth_list = []
        elevent_list = []
        twelfth_list = []

        months_dict = {}


        data = requests.get('https://api.marketstack.com/v1/eod?access_key='+api_key+'&symbols='+item+'&date_from=2013-01-01&date=2020-01-01&limit=1000')
        stock_data = json.loads(data.text)
    


        for dic in range(len(stock_data['data'])):

         #find just the date, not the time

            date = (re.search("(\d\d\d\d-\d\d-\d\d)", stock_data['data'][dic]['date'])).group()
       
       #might not need if statement below
        #if date in dates:

            temp_dict['date']  = date

        

       
            temp_dict['close'] =  stock_data['data'][dic]['close']

            temp_dict['volume'] =  stock_data['data'][dic]['volume']
       

            date_close_list.append(temp_dict)

            temp_dict = {}


    
        

    date_close_list =  organize_by_year_month(date_close_list)



    

    for year,d in date_close_list.items():
        for month,close in d.items():
            
            date_close_list[year][month] = find_average_of_list(close)


 
    print(date_close_list)
    
    return(date_close_list)
    pass



        
        
"""
#DOESNT CALCULATE BY YEAR 

        for d in date_close_list:

            if d['date'][0:4] == '2022' :

                jan_list.append(d)
         
            
            
            if d['date'][5:7] == '01' :

                jan_list.append(d)

            if d['date'][5:7] == '02' :

                feb_list.append(d)
            
            if d['date'][5:7] == '03' :

                mar_list.append(d)


            if d['date'][5:7] == '04' :

                apr_list.append(d)


            if d['date'][5:7] == '05' :

                may_list.append(d)


            if d['date'][5:7] == '06' :

                jun_list.append(d)

            if d['date'][5:7] == '07' :

                jul_list.append(d)

            if d['date'][5:7] == '08' :

                aug_list.append(d)

            if d['date'][5:7] == '09' :

                sept_list.append(d)

            if d['date'][5:7] == '10' :

                oct_list.append(d)

            if d['date'][5:7] == '11' :

                nov_list.append(d)

            if d['date'][5:7] == '12' :

                dec_list.append(d)



            
            
        months_dict['Jan'] = find_average_of_list(jan_list)
        
        months_dict['Feb'] = find_average_of_list(feb_list)
      
        months_dict['Mar'] = find_average_of_list(mar_list)
        
        months_dict['Apr'] = find_average_of_list(apr_list)
        months_dict['May'] = find_average_of_list(may_list)
        months_dict['Jun'] = find_average_of_list(jun_list)
        months_dict['Jul'] = find_average_of_list(jul_list)
        months_dict['Aug'] = find_average_of_list(aug_list)
        months_dict['Sept'] = find_average_of_list(sept_list)
        months_dict['Oct'] = find_average_of_list(oct_list)
        months_dict['Nov'] = find_average_of_list(nov_list)
        months_dict['Dec'] = find_average_of_list(dec_list)
           


        



        final_dict[stock_data['data'][dic]['symbol']] = months_dict

    print(final_dict)

        

        #print(stock_data['data'][dic]['symbol'] + ": "+stock_data['data'][dic]['date'] + ": " + str(stock_data['data'][dic]['close']))

    return(final_dict)


    #print(stock_data)


    #data_2 = requests.get('https://api.marketstack.com/v1/eod?access_key='+api_key+'&symbols=AAPL&date_from=2013-01-01&date=2020-01-01&limit=1000&offset=1000')
    
    #stock_data_2 = json.loads(data_2.text)
    



    

    #for dic in range(len(stock_data_2['data'])):
       # print(stock_data_2['data'][dic]['date'] + ": " + str(stock_data_2['data'][dic]['close']))
    
"""

    

    

    
  
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


def drop_table(db_filename):
    con = sqlite3.connect(db_filename)
    cur = con.cursor()

    cur.execute("DROP TABLE dates")
    con.commit()

if __name__ == '__main__':

    tickers = get_spy_data('https://stockmarketmba.com/stocksinthesp500.php')
  
    get_crypto_data()
    data = get_stock_data(tickers,get_economic_data())

   # drop_table('final_project.db')

    create_dates_table(data,'final_project.db')



    
    





    unittest.main(verbosity=2)