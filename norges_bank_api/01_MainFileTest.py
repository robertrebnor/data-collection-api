#########################################################
###                                                   ###
###                  The Main Program                 ###
###                                                   ###                     
#########################################################

# comment F:
#Gjerne også noe helt oppe i toppen av programmet ditt, sånn at du kjører en start() eller noe, og så har du 
# try catch rundt den også, så kan du håndtere at programmet ditt krasjer og feks starte det på nytt tre ganger 
# før du gir opp og gir en feilmelding ala "programmet prøvde å starte tre ganger men krasjet pga : {feilmelding}"

# Så dumper du alt det til en tekstfil ala logg.tx



import pandas as pd
import InitializeData as InitiData 
import support_functions as support
import api_data as api_data

#########################################################
###                                                   ###
###                 1. Initialize dataset             ###
###                                                   ###                     
#########################################################

# Enter the filepath to the dataset
DataPath = r"Data\EXR.csv"
# Enter the file type of the dataset
FileType = "csv"
# Enter if there is a specific sheet in Execl to read in
sheetName = None
# index col
index_col ="date" 

## Testing multiple inheritance, using the "SetUpFile" to initialize 
#testData_df = InitiData.ReadInDataFile(DataPath, FileType, sheetName, index_col) 
testData_df = InitiData.ReadInDataFile(DataPath, FileType, sheetName) 
#testData_df.reset_index()

# Fix the date type:
#testData_df['date'] = testData_df['date'].astype('datetime64[ns]')
testData_df['date'] = pd.to_datetime(testData_df['date'])

#testData_df.dtypes

### find out what day it is to day, and how many day's are missing in the dataset:
# use pandas Timestap to get today's day:
today = pd.Timestamp('today')

# find the newest day in the dataset:
#testData_df['date'].iloc[-1]
last_day_df = testData_df['date'].iloc[-2]

delta = today - last_day_df
print(delta.days)


# Test a print to filepath:
InitiData.Df_toFile(testData_df, r"Data\EXR_update.xlsx", "excel")


#############################################################################
## Go to the real deal:
# So I know have  dataset, EXR_update.xlsx that I need to update

# Step 1: Read in the dataset: 
DataPath = r"Data\EXR_update.xlsx"
# Enter the file type of the dataset
FileType = "excel"

Update_df = InitiData.ReadInDataFile(DataPath, FileType) 
Update_df

### test missing dates:
number_of_days = support.missing_dates(Update_df)

# get the last observations using a specific number of days 
new_observations_df = api_data.norwegian_bank_exchange_rate_api(number_of_days)
new_observations_df


### Update the df, by using last observed day in df and today's date:

def update_data_exchange_rate_nb(original_df):
    # start by getting the first missing day in the df:
    first_missing_day = support.df_next_day(original_df)

    # get the exchange rates from the missing dates:
    new_observations_df = api_data.norwegian_bank_exchange_rate_api(0,first_missing_day)

    # Append together the old and new obs:
    updated_df = support.append_new_obs(original_df, new_observations_df)
    print('Dataframe updated.')
    InitiData.Df_toFile(updated_df, r"Data\EXR_update.xlsx", "excel")
    print('Dateframe updated in Excel')

    return updated_df

new_df = update_data_exchange_rate_nb(Update_df)
