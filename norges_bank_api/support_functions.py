import datetime



def missing_dates(df, name_date_col = 'date'): 
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



def df_next_day(df, date_name = 'date'):
    # Gets the last day in the dataframe, and adds 1 day to get the first missing day. 
    # Returns the date in a string format to fit the use in the API url request.
    last_date = df[date_name].dt.date
    last_date = str(last_date[len(last_date)-1] + datetime.timedelta(days=1)  ) #gets the last day in the df and adds one day to get the first date I want a date for
    return last_date


def append_new_obs(orginal_df, new_df):
    # Appends the new dataframe with observations at the end of the old one. 
    # Fixes the row indexes. 
    df_appended = orginal_df.append(new_df)
    df_appended.reset_index(drop=True, inplace=True)
    return df_appended


    


