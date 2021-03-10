## Reading data from online 

import requests
import json
import pandas as pd

def NorgesBankAPI(days):
    # Given a number of days, reads in 40 exchange rates from Norges Bank

    # should fix the "str_start" such that I can choose which of the 40 ER that I want to get
    str_start = "https://data.norges-bank.no/api/data/EXR/B.USD+AUD+BDT+GBP+BRL+BGN+DKK+EUR+PHP+HKD+XDR+I44+INR+IDR+TWI+ISK+JPY+CAD+CNY+HRK+MYR+MXN+MMK+NZD+RON+ILS+BYN+TWD+PKR+PLN+RUB+SGD+CHF+SEK+ZAR+KRW+THB+CZK+TRY+HUF.NOK.SP?format=sdmx-json&lastNObservations="
    str_end = "&locale=no"
    str_days = str(days)
    url = str_start + str_days + str_end

    response =  requests.get(url)
    print(response.status_code)

    #fix and format data:
    data_new = json.loads(response.text)

    # create a dataframe:
    df_updated_data = pd.DataFrame()

    # Get the dates in the first col:
    for i in range(days):
        unpack = data_new['data']['structure']['dimensions']['observation'][0]['values'][i]
        df_updated_data = df_updated_data.append( pd.DataFrame.from_dict(unpack, orient = 'index') )
    df_updated_data = df_updated_data.drop(index = ['start', 'end','name'])
    df_updated_data.reset_index(drop=True, inplace=True)
    df_updated_data.rename(columns={0: "date"},inplace =True)
    df_updated_data['date'] = df_updated_data['date'].astype('datetime64[ns]')

    #Get a list of the alpha3 currency codes:
    number_currencies = 40 
    name_currencies = []
    for i in range(number_currencies):
        name_currencies.append(data_new['data']['structure']['dimensions']['series'][1]['values'][i]['id'])
    
    # Get the observations:
    currency_keys = list(data_new['data']['dataSets'][0]['series'].keys()) #gives 40 key's 
    
    count = 0 #to keep track of the number in the currency_keys and name_currencies
    for x in currency_keys:
        # get a list of a given currency series
        currency_values_temp = list(data_new['data']['dataSets'][0]['series'][x]['observations'].values())
        # fix the list:
        for i in range(len(currency_values_temp)):
            currency_values_temp[i] = currency_values_temp[i][0]
        # Append a col in the df with colname alpha3-code and observations
        df_updated_data[ name_currencies[count] ] = currency_values_temp
        # Fix the variable type from object to float
        df_updated_data[ name_currencies[count] ] = df_updated_data[ name_currencies[count] ].astype('float64')
        count += 1    
    return df_updated_data    

#testing:
#days = 30
#df = NorgesBankAPI(days)
#print(df)
