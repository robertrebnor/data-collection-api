## Reading data from online 

# https://data.norges-bank.no/api/data/EXR/B.EUR.NOK.SP?format=csv&lastNObservations=40&locale=no&bom=include

# https://www.dataquest.io/blog/python-api-tutorial/

# Må kunne i JSON:
#   Lag re litt data i json, hent ut igjen, se hva som er gyldig format. serialisere (json til tekst) og deserialisere (tekst tilbake til json)


import requests
import json
import pandas as pd


def NorgesBankAPI(days):
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
    df_updated_data.rename(columns={0: "data"},inplace =True)

    # observations
    data_new_obs = data_new['data']['dataSets'][0]['series']['0:0:0:0']['observations']
    data_new_obs =  pd.DataFrame.from_dict(data_new_obs, orient = 'index')

    # get the dates 
    #data_new_dates = pd.DataFrame()
    #for i in range(days):
    #    unpack = data_new['data']['structure']['dimensions']['observation'][0]['values'][i]
    #    data_new_dates = data_new_dates.append( pd.DataFrame.from_dict(unpack, orient = 'index') )
    #data_new_dates = data_new_dates.drop(index = ['start', 'end','name'])

    # combine in one df
    data_new_dates['eur'] = data_new_obs[0].values

    # fix:
    data_new_dates.rename(columns={0: 'date'}, inplace = True)
    data_new_dates['eur'] = data_new_dates['eur'].astype('float64')
    data_new_dates['date'] = data_new_dates['date'].astype('datetime64[ns]')
    
    return data_new_dates

#testing:
days = 30
df = NorgesBankAPI(days)
print(df)
df.dtypes

### need to test the new api with all the 40 ER:

days = 10
str_start = "https://data.norges-bank.no/api/data/EXR/B.USD+AUD+BDT+GBP+BRL+BGN+DKK+EUR+PHP+HKD+XDR+I44+INR+IDR+TWI+ISK+JPY+CAD+CNY+HRK+MYR+MXN+MMK+NZD+RON+ILS+BYN+TWD+PKR+PLN+RUB+SGD+CHF+SEK+ZAR+KRW+THB+CZK+TRY+HUF.NOK.SP?format=sdmx-json&lastNObservations="
str_end = "&locale=no"
str_days = str(days)
url = str_start + str_days + str_end

response =  requests.get(url)
print(response.status_code)

#fix and format data:
data_new = json.loads(response.text)

# seek for the observations:
data_new['data']['dataSets'][0]['series'].keys() #gives 40 key's 
list(data_new['data']['dataSets'][0]['series']['0:0:0:0']['observations'].values()) #need to iterate over str(0:0:0:0) from 0 - 39

testing_values = list(data_new['data']['dataSets'][0]['series']['0:0:0:0']['observations'].values())
testing_values[3]

list_observations_iterations = ['0:0:0:0', '0:1:0:0', '0:2:0:0', '0:3:0:0', '0:4:0:0', '0:5:0:0', '0:6:0:0', '0:7:0:0', '0:8:0:0', '0:9:0:0', '0:10:0:0', '0:11:0:0', '0:12:0:0', '0:13:0:0', '0:14:0:0', '0:15:0:0', '0:16:0:0', '0:17:0:0', '0:18:0:0', '0:19:0:0', '0:20:0:0', '0:21:0:0', '0:22:0:0', '0:23:0:0', '0:24:0:0', '0:25:0:0', '0:26:0:0', '0:27:0:0', '0:28:0:0', '0:29:0:0', '0:30:0:0', '0:31:0:0', '0:32:0:0', '0:33:0:0', '0:34:0:0', '0:35:0:0', '0:36:0:0', '0:37:0:0', '0:38:0:0', '0:39:0:0']


list(data_new['data']['dataSets'][0]['series'].keys())

# fin the name of the ER
data_new['data']['structure']['dimensions']['series'][1]['values'][0]['id'] # iterate over [0] from 0 to 39 to get the iso-code for currencies


# observations
data_new_obs = data_new['data']['dataSets'][0]['series']['0:0:0:0']['observations']
data_new_obs =  pd.DataFrame.from_dict(data_new_obs, orient = 'index')

# get the dates 
df_updated_data = pd.DataFrame()
for i in range(days):
    unpack = data_new['data']['structure']['dimensions']['observation'][0]['values'][i] # the path for dates
    df_updated_data = df_updated_data.append( pd.DataFrame.from_dict(unpack, orient = 'index') ) #get the dates directly into the df
df_updated_data = df_updated_data.drop(index = ['start', 'end','name']) # I get four dates obs per day, removes these three
df_updated_data.reset_index(drop=True, inplace=True) #removes 'id' as the index
df_updated_data.rename(columns={0: "data"},inplace =True) #fix the name of the col to 'date'
# Now the 'id' is the index

# Get the name of the currencies: 
number_currencies = 40
for i in range(number_currencies):
    data_new['data']['structure']['dimensions']['series'][1]['values'][0]['id']
data_new['data']['structure']['dimensions']['series'][1]['values'][0]['id'] # iterate over [0] from 0 to 39 to get the iso-code for currencies

# combine in one df, should change this, so that I copy the dates into the frame with all the currencies 
data_new_dates['eur'] = data_new_obs[0].values

# fix:
data_new_dates.rename(columns={0: 'date'}, inplace = True)
data_new_dates['eur'] = data_new_dates['eur'].astype('float64')
data_new_dates['date'] = data_new_dates['date'].astype('datetime64[ns]')
    



























































######################################################################################################################################3
# put the link in a variable 
# add a variable to change "40" into a number of my choice

response = requests.get("https://data.norges-bank.no/api/data/EXR/B.EUR.NOK.SP?format=sdmx-json&lastNObservations=40&locale=no")


#response_csv = requests.get("https://data.norges-bank.no/api/data/EXR/B.EUR.NOK.SP?format=csv&lastNObservations=40&locale=no&bom=include")
#print(response_csv.text)

# check the request
print(response.status_code)

print(response.text)

print(response.json())

# https://realpython.com/python-json/

# make a Python dict: 
data = json.loads(response.text)

#data.keys()

#data.get('meta')
#data.get('data')


#data['data'].keys()

#data['data']['dataSets'].keys()
#data['data']['structure'].keys()

#data['data']['dataSets'].index('OBS_VALUE')

# this works to get the exchange rates
rec = data['data']['dataSets'][0]['series']['0:0:0:0']['observations']
#df = pd.json_normalize(rec)
#df = df.T
#print(df)

# this is the best way to extract the dict into a df:
df =  pd.DataFrame.from_dict(rec, orient = 'index')

# Rest of the information: 
len(data['data']['structure']['dimensions']['observation'][0]['values']) # list length = 40 equal the same as in the request

# Read:
# https://stackoverflow.com/questions/13784192/creating-an-empty-pandas-dataframe-then-filling-it

# This gives a list of the dates. 
dt_dates = pd.DataFrame() 
# to get the dates:
for i in range(40): #change 40 to the length of observations requested
    unpack = data['data']['structure']['dimensions']['observation'][0]['values'][i]
    dt_dates = dt_dates.append( pd.DataFrame.from_dict(unpack, orient = 'index') )
print('done')
dt_dates = dt_dates.drop(index = ['start', 'end','name'])
print(dt_dates)

dt_dates['eur'] = df[0].values
print(dt_dates)




 
unpack = data['data']['structure']['dimensions']['observation'][0]['values'][1]['id']
test11 = pd.DataFrame.from_dict(unpack, orient = 'index')
test11 = test11.append( pd.DataFrame.from_dict(unpack, orient = 'index') )
type(unpack)

#
import requests
import pandas as pd

from pandas import json_normalize
url = 'https://www.energidataservice.dk/proxy/api/datastore_search?resource_id=nordpoolmarket&limit=5'

response = requests.get("https://data.norges-bank.no/api/data/EXR/B.EUR.NOK.SP?format=sdmx-json&lastNObservations=40&locale=no")


dictr = response.json()
recs = dictr['data']['structure']
df = pd.json_normalize(recs)
print(df)

dictr.keys()

dictr['data']


### Test the API csv to Pandas df:


#response2 = requests.get("https://data.norges-bank.no/api/data/EXR/B.EUR.NOK.SP?format=csv&lastNObservations=40&locale=no&bom=include")
#print(response2.status_code)
#currencies = pd.read_csv(response2.text)


test1 = 11
type(test1)

test1 = str(test1)
type(test1)


