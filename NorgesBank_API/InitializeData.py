#########################################################
###                                                   ###
###           Initialize Data                         ###
###                                                   ###                     
#########################################################
"""Overview of the program:

    Goal:
    -----
    *Initialize data into a dataframe
    *Format the dataframe and set appropriate types to columns 
    
    Functions:
    ----------
    __init__: Creates a dataframe, prints basic info
    returnDf: Return the dataframe
    basicInfo: 
 
"""
import pandas as pd

def ReadInDataFile(DataPath, FileType, sheetName=None, index_col=None):
    """
    Creates a dataframe from a datafile. Prints basic info,
    such as rows, cols, head, col names and variable types.

    Parameters
    ----------
    DataPath:  string
        the path to the file.
    FileType: string
        Says which filetype to read in.
        Options are: "excel" and "csv"
    sheetName: string
        If filetype is Excel and there are multiple sheets within the Excel file,
        sheetName specifies which sheet to read in.
        By default sheetName is sat to empty.
    Output
    ------
    A dataframe from Pandas
    """
    if FileType == "excel" and sheetName == None:
        df = pd.read_excel(DataPath)
    elif FileType == "excel" and sheetName != None:
        df = pd.read_excel(DataPath, sheet_name = sheetName)
    elif FileType == "csv":
        df = pd.read_csv(DataPath, index_col = index_col)
    print("")
    print("Dataframe created.")
    return(df)


def Df_toFile(df, DataPath, FileType, sheetName=None):
    if FileType == "excel" and sheetName == None:
        df.to_excel(DataPath, index=False)
    elif FileType == "excel" and sheetName != None:
        df.to_excel(DataPath, sheet_name = sheetName, index=False)
    elif FileType == "csv": 
        df.to_csv(DataPath) #do I need something like this here?
    print("Dataframe save at: ", DataPath)