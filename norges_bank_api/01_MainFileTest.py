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


import InitializeData as InitiData 
import pandas as pd

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



## Go to the real deal:
# So I know have  dataset, EXR_update.xlsx that I need to update

# Step 1: Read in the dataset: 
DataPath = r"Data\EXR_update.xlsx"
# Enter the file type of the dataset
FileType = "excel"

Update_df = InitiData.ReadInDataFile(DataPath, FileType) 
Update_df


def MissingDates(df, name_date_col = 'date'): 
    #transform the dateformat in the df (write a check if I need to change this)
    df[name_date_col] = pd.to_datetime(df[name_date_col])
    # get the last day observered:
    last_obs_day = df[name_date_col].iloc[-1]
    # get today's date:
    today = pd.Timestamp('today')

    #calc the difference:
    missing_dates = (today - last_obs_day).days

    print('The dataframe is missing', missing_dates ,'number of dates.')
    return missing_dates

#test missing dates:
MissingDates(Update_df)