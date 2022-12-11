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
      
    # Append the datapoint to the list of data for the year and month
    organized_data[year][month].append(datapoint)
  
  # Return the organized data
  return organized_data



if __name__ == '__main__':
    data = [{'date': '2022-01-31', 'close': 174.78}, {'date': '2022-02-28', 'close': 170.33}, {'date': '2022-04-27', 'close': 159.22}]
print(organize_by_year_month(data))

