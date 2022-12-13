import  requests
from xml.sax import parseString
from bs4 import BeautifulSoup
import json
import re
import csv
import numpy as np
import matplotlib.pyplot as plt
import os
import sqlite3
import unittest
import unittest
from datetime import datetime
from sklearn.linear_model import LinearRegression






def get_spy_data():

    #link to website

    link = 'https://stockmarketmba.com/stocksinthesp500.php'

    tickers_dic ={}

    
    page = requests.get(link)

    soup = BeautifulSoup(page.content, "html.parser")

    rows = soup.find_all("tr")

    

    #go through each column

    for row in rows[1:]:

        columns = row.find_all("td",None)

        ticker_link = columns[0]

        marketcap = columns[5]

        ticker = ticker_link.find("a",None)

   
        if ticker != None:

            marketcap = int(marketcap.text.replace(',','').strip('$'))
            ticker = ticker.text

            tickers_dic[ticker] = marketcap

            tickers_list_sorted = sorted(tickers_dic.items(), key=lambda x:x[1], reverse=True)

    

    #return sorted list
    return(tickers_list_sorted)

    




    pass

 

def get_economic_data():
    key = '0826dcd62489d3c9b0e3a3d14dea492b'


    organized_dict = {}

    cpi = requests.get('https://api.stlouisfed.org/fred/series/observations?series_id=CPILFESL&api_key='+key+'&file_type=json&observation_start=2013-01-01')

    cpi_data = json.loads(cpi.text)


    organized_dict =  make_list_of_dictionaries(cpi_data)
    

    organized_dict = dict(sorted(organized_dict.items(), key=lambda x: x[0], reverse=True))

    for year,months in organized_dict.items():
        organized_dict[year] = dict(sorted(months.items(), key=lambda x: x[0], reverse=True))



   
    return(organized_dict)
    
   
    pass
  



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

    
    api_key = '28fc4e3838a1dd4a6a9cfa76630cdb7a'
    tickers_list = []
    

   
    

    organized_list = []
    
    

    

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

    
    

    organized_list = make_list_of_dictionaries(stock_data)
   



    

    for year,d in organized_list.items():
        for month,close in d.items():
            
            organized_list[year][month] = find_average_of_list(close)
    
    
    return(organized_list)


def create_dates_table(stock_dict, db_filename):
    
    con = sqlite3.connect(db_filename)
    cur = con.cursor()

    month_dict = {	1:'January',
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

    cur.execute("SELECT id FROM dates WHERE id = (SELECT MAX(id) FROM dates)")
    start = cur.fetchone()
    
    if (start != None):
        start = start[0]+1
    else:
        start = 1


    i = 1
    
    for year,data in stock_dict.items():
        for month,close in data.items():
            if (i >= start and i< (start+25)):
                date = (str(month_dict[month])+", " + str(year))
                cur.execute("INSERT OR IGNORE INTO dates(date) VALUES (?)", [date])
            i +=1

    



        
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




def create_economic_table(economic_dict,db_filename):

    con = sqlite3.connect(db_filename)
    cur = con.cursor()

    

    

    cur.execute("CREATE TABLE IF NOT EXISTS economic_info (id INTEGER PRIMARY KEY, value DOUBLE)")
    
    cur.execute("SELECT id FROM economic_info WHERE id = (SELECT MAX(id) FROM economic_info)")
    start = cur.fetchone()
    
    if (start != None):
        start = start[0]+1
    else:
        start = 3


    i = 3

    

    for year,data in economic_dict.items():
        for month,val in data.items():
            if (i >= start and i< (start+25)):
                value = val[0]['value']
                
                
                
                cur.execute("INSERT OR IGNORE INTO economic_info(id,value) VALUES (?,?)", (i,value))
            i +=1
    con.commit()




#CALCULATIONS SECTION


def calculate_inflation_rate(db_filename):
    con = sqlite3.connect(db_filename)
    cur = con.cursor()

    percent_increase_list = []


    data = cur.execute('SELECT dates.date,economic_info.value FROM economic_info INNER JOIN dates ON economic_info.id = dates.id')

    data = data.fetchall()

    file_exists = os.path.exists('calculations.txt')

    if file_exists:
        aw = 'a'

    else:
        aw = 'w'



    with open('calculations.txt', aw) as f:

        
    

        f.write("\nPERCENTAGE CHANGE IN INFLATION EACH MONTH FOR 10 YEARS:\n")

        f.write("____________________________________\n")

        f.write("Equation: (Second month CPI - first month CPI)/first month CPI)*100 \n")
        f.write("Example:() (20 - 10)/(10)*100) = 100% | The inflation rate percentage is 100% \n")


        f.write(f'{"Start Date":{20}} {"End Date":{20}} {"Inflation Increase Percent:":{7}}\n') 

    
        for row_number in range(1,len(data)):

        




       
            date_one = data[row_number-1][0]
            date_two = data[row_number][0]

        
        
            original = data[row_number-1][1]
            next = data[row_number][1]

 


  
            percent_increase = round((((original - next)/next)*100),2)

            percent_increase_list.append(percent_increase)

            f.write(f'{date_one:{20}} {date_two:{20}} {str(percent_increase)+"%":{7}}\n') 
    return(percent_increase_list)


    pass









    pass



def calculate_percent_change(db_filename,table_name):

    con = sqlite3.connect(db_filename)
    cur = con.cursor()

    percent_increase_list = []

    data = cur.execute('SELECT dates.date,'+table_name+'.ticker,'+table_name+'.avg_close FROM '+table_name+' INNER JOIN dates ON '+table_name+'.id = dates.id')

    data = data.fetchall()

    ticker = data[0][1]

    file_exists = os.path.exists('calculations.txt')

    if file_exists:
        aw = 'a'

    else:
        aw = 'w'

    with open('calculations.txt', aw) as f:

        f.write("\nPERCENTAGE INCREASE FOR " + ticker + " EACH MONTH FOR 10 YEARS:\n")
        f.write("____________________________________\n")
        f.write("Equation: (Second month price - first month price)/first month price)*100 \n")
        f.write("Example:() ($20 - $10)/($10)*100) = 100% \n")



        f.write(f'{"Ticker":{10}} {"Start Date":{20}} {"End Date":{20}} {"Percentage Increase":{12}}\n') 

    
        for row_number in range(1,len(data)):

        




       
            date_one = data[row_number-1][0]
            date_two = data[row_number][0]

        
        
            original = data[row_number-1][2]
            next = data[row_number][2]

 


  
            percent_increase = round((((original - next)/next)*100),2)

            percent_increase_list.append(percent_increase)

            f.write(f'{ticker:{10}} {date_one:{20}} {date_two:{20}} {str(percent_increase)+"%":{7}}\n') 

        #print("The percent increase for "+ticker+" between "+ date_two + " and " + date_one +" is "+ str(percent_increase) + "%")
    
    return(percent_increase_list)
    pass


def calculate_total_average(db_filename):
        con = sqlite3.connect(db_filename)
        cur = con.cursor()

        average  = cur.execute("SELECT stock_info.ticker,AVG(stock_info.avg_close),crypto_info.ticker,AVG(crypto_info.avg_close) FROM stock_info,crypto_info") # INNER JOIN categories ON restaurants.category_id = categories.id GROUP BY restaurants.category_id")
        

        average = average.fetchall()[0]

        ticker_1 = average[0]
        price_1 = str(round(average[1],2))
        ticker_2 = average[2]
        price_2 = str(round(average[3],2))

        file_exists = os.path.exists('calculations.txt')

        if file_exists:
            aw = 'a'

        else:
            aw = 'w'

        with open('calculations.txt', aw) as f:

            f.write("\nTHE AVERAGE COSTS OF " + ticker_1 + " AND " + ticker_2 + " OVER THE PAST 10 YEARS\n")
            f.write("____________________________________\n")
            f.write("FOUND USING AVG FUNCTION PROVIDED IN SQL\n")

            f.write(f'{"TICKER":{7}} {"AVERAGE COST":{11}}\n') 
            f.write(f'{ticker_1:{7}} {"$"+ price_1:.>{11}}\n') 
            f.write(f'{ticker_2:{7}} {"$"+ price_2:.>{11}}\n') 

pass

        
            

#VISUALIZATIONS 

def price_visualization(db_filename,table_name):

    date_list = []
    price_list = []
    date_num_list = []
    vol_list = []

    con = sqlite3.connect(db_filename)
    cur = con.cursor()

    data = cur.execute('SELECT dates.date,'+table_name+'.ticker,'+table_name+'.avg_close,'+table_name+'.avg_vol FROM '+table_name+' INNER JOIN dates ON '+table_name+'.id = dates.id')

    data = data.fetchall()

    ticker = data[0][1]
   

    for row_number in range(0,len(data)):

        date_list.append(data[row_number][0]) 

        price_list.append(data[row_number][2]) 

        vol_list.append(data[row_number][3])

        
    


    i = 0

    for item in date_list:
        date_num_list.append(i)
        i +=1


    

    price_list.reverse()
    date_list.reverse()
    vol_list.reverse()




    
    plot1 = plt.subplot2grid((25, 10), (0, 0), colspan=10,rowspan = 10)
    plot2 = plt.subplot2grid((25, 10), (15, 0), colspan=10,rowspan = 10)
    

    
   

    x = np.array(date_num_list)
    y = np.array(price_list)

    y2 = np.array(vol_list)

   

    a, b = np.polyfit(x, y, 1)

    a2,b2 = np.polyfit(x,y2,1)


    plot1.scatter(x,y,color = 'green')
    plot1.plot(date_list, a*x+b, color='steelblue', linestyle='--', linewidth=2)
    plot1.text(100, 50, 'y = ' + '{:.2f}'.format(b) + ' + {:.2f}'.format(a) + 'x', size=10)
    plot1.set_title('Average Price for ' +ticker+ ' Each Month Since 2013')
    plot1.set_ylabel('Average Price')
    plot1.set_xlabel('Month and Year')
    plot1.set_xticklabels(date_list, rotation=45,size = 4)


    plot2.scatter(x,y2,color = 'orange')
    plot2.plot(date_list, a2*x+b2, color='green', linestyle='--', linewidth=2)
    if ticker == 'AAPL':
        plot2.text(1, 80000000, 'y = ' + '{:.2f}'.format(b2) + ' + {:.2f}'.format(a2) + 'x', size=10)
    else:
        plot2.text(1, 100000, 'y = ' + '{:.2f}'.format(b2) + ' + {:.2f}'.format(a2) + 'x', size=10)

    plot2.set_title('Average Volume for '+ ticker+ ' Each Month Since 2013')
    plot2.set_ylabel('Average Volume')
    plot2.set_xlabel('Month and Year')
    plot2.set_xticklabels(date_list, rotation=45,size = 4)

   
    

    

   

    

    #plt.scatter(x,y,color = 'green')

    #plt.plot(date_list, a*x+b, color='steelblue', linestyle='--', linewidth=2)

    #plt.text(1, 160, 'y = ' + '{:.2f}'.format(b) + ' + {:.2f}'.format(a) + 'x', size=14)



    

  

    plt.draw()

   


    plt.show()


    pass


def inflation_visualization(db_filename,table_name,percent_change_list):

    date_list = []
    cpi_list = []
    date_num_list = []
    percent_num_list = []
    

    con = sqlite3.connect(db_filename)
    cur = con.cursor()

    data = cur.execute('SELECT dates.date,'+table_name+'.value FROM '+table_name+' INNER JOIN dates ON '+table_name+'.id = dates.id')

    data = data.fetchall()


   

    for row_number in range(0,len(data)):

        date_list.append(data[row_number][0]) 

        cpi_list.append(data[row_number][1]) 

        

        
    
    #print(date_list)

    i = 0

    for item in date_list:
        date_num_list.append(i)
        i +=1


    

    
    date_list.reverse()
    cpi_list.reverse()




    
    plot1 = plt.subplot2grid((25, 10), (0, 0), colspan=10,rowspan = 10)
    plot2 = plt.subplot2grid((25, 10), (15, 0), colspan=10,rowspan = 10)
    

    
   

    x = np.array(date_num_list)
    y = np.array(cpi_list)

    z = 0

    for item in range(len(percent_change_list)):
        percent_num_list.append(z)
        z += 1

    x2 = np.array(percent_num_list)

    y2 = np.array(percent_change_list)

   

    a, b = np.polyfit(x, y, 1)

    a2,b2 = np.polyfit(x2,y2,1)


    plot1.scatter(x,y,color = 'green')
    plot1.plot(date_list, a*x+b, color='steelblue', linestyle='--', linewidth=2)
    plot1.text(100, 50, 'y = ' + '{:.2f}'.format(b) + ' + {:.2f}'.format(a) + 'x', size=10)
    plot1.set_title('CPI Each Month For 10 Years')
    plot1.set_ylabel('CPI')
    plot1.set_xlabel('Month and Year')
    plot1.set_xticklabels(date_list, rotation=45,size = 4)


    plot2.scatter(x2,y2,color = 'orange')
    plot2.plot(x2, a2*x2+b2, color='green', linestyle='--', linewidth=2)
   
    plot2.text(1, 8, 'y = ' + '{:.2f}'.format(b2) + ' + {:.2f}'.format(a2) + 'x', size=10)

    plot2.set_title('Change IN CPI Each Month')
    plot2.set_ylabel('Percent Change')
    plot2.set_xlabel('Month and Year')
    plot2.set_xticklabels(percent_num_list, rotation=45,size = 4)

    plt.draw()

   


    plt.show()


pass




def asset_inflation_visualization(cpi_list, btc_list,stock_list):

    z = 0

    num_list = []

    for item in range(len(cpi_list)):
        num_list.append(z)
        z += 1


    


    x = np.array(num_list)

    y1 = np.array(cpi_list)
   
    y2 = np.array(btc_list[0:117])

    y3 = np.array(stock_list[0:117])


  

  

    plt.plot(x, y1, color='r', label='Inflation')
    plt.plot(x, y2, color='g', label='BTC')
    plt.plot(x, y3, color='b', label='STOCK')
  

    plt.xlabel("TIME")
    plt.ylabel("PERCENT CHANGE")
    plt.title("PERCENT CHANGE VS TIME")

    plt.legend()
  

    plt.show()

   
    

    

   

    

  



    

  

   






def restart(db_filename):
    con = sqlite3.connect(db_filename)
    cur = con.cursor()

    cur.execute("DROP TABLE dates")
    cur.execute("DROP TABLE stock_info")
    cur.execute("DROP TABLE crypto_info")
    cur.execute("DROP TABLE economic_info")
    os.remove("calculations.txt")
    con.commit()


#HELPER FUNCTIONS


def organize_by_year_month(data):
  
  organized_data = {}
  

  for datapoint in data:
  
    
    date = datetime.strptime(datapoint['date'], '%Y-%m-%d')
  

    

    year = date.year
    month = date.month
    
    
    if year not in organized_data:
      organized_data[year] = {}
    if month not in organized_data[year]:
      organized_data[year][month] = []
      

    organized_data[year][month].append(datapoint)


    
  




  
  return organized_data


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


if __name__ == '__main__':

    val = 1




    if val == 1:
        tickers = get_spy_data()
        economic_data = get_economic_data()
  
        crypto_data = get_crypto_data()
        stock_data = get_stock_data(tickers)

    

        create_dates_table(stock_data,'final_project.db')
        create_stock_table(stock_data,'final_project.db')
        create_crypto_table(crypto_data,'final_project.db')
        create_economic_table(economic_data,'final_project.db')


     
        con = sqlite3.connect('final_project.db')
        cur = con.cursor()
        max = cur.execute("SELECT id FROM dates WHERE id = (SELECT MAX(id) FROM dates)")
        max = cur.fetchone()
        max = max[0]
     
        if (max == 120):
            stock_percent = calculate_percent_change('final_project.db',"stock_info")
            crypto_percent = calculate_percent_change('final_project.db',"crypto_info")
            inflation = calculate_inflation_rate('final_project.db')
            calculate_total_average('final_project.db')


        #visualizations

            price_visualization('final_project.db',"stock_info")
            price_visualization('final_project.db',"crypto_info")
            inflation_visualization('final_project.db','economic_info',inflation)
            asset_inflation_visualization(inflation,crypto_percent,stock_percent)


        pass

    else:
        restart('final_project.db')
        pass




    
    





    unittest.main(verbosity=2)