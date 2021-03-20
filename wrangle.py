import pandas as pd
import numpy as numpy
from env import host, user, password 
import os

from sklearn.model_selection import train_test_split
import sklearn.preprocessing





############################# Acquire Zillow ############################# 

# defines function to create a sql url using personal credentials
def get_connection(db, user=user, host=host, password=password):
    '''
    This function uses my info from my env file to
    create a connection url to access the Codeup db.
    '''
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'


# defines function to get zillow data from MySQL and return as a pandas DataFrame
def get_zillow_data():
    '''
    This function reads in the zillow data from the Codeup db,
    selects all columns from the properties_2017 table,
    joins predictions_2017 table,
    and acquires single unit properties with transactions during May 2017 - August 2017
    and returns a pandas DataFrame with all columns.
    '''
 
    #create SQL query
    sql_query = '''
                SELECT *
                FROM properties_2017
                JOIN predictions_2017 USING(parcelid)
                WHERE propertylandusetypeid IN (260, 261, 263, 264, 265, 266, 273, 275, 276, 279)
                AND transactiondate >= "2017-05-01" AND transactiondate <= "2017-08-31";
                '''
    
    #read in dataframe from Codeup db
    df = pd.read_sql(sql_query, get_connection('zillow'))
    
    return df


# adds caching to get_titanic_data and checks for local filename (titanic.csv)
# if file exists, uses the .csv file
# if file doesn't exist, then produces SQL & pandas necessary to create a df, then write the df to a .csv file
def cached_zillow(cached=False):
    '''
    This function reads in zillow data from Codeup database and writes data to
    a csv file if cached == False or if cached == True reads in zillow df from
    a csv file, returns df.
    ''' 
    if cached == False or os.path.isfile('zillow_df.csv') == False:
        
        # Read fresh data from db into a DataFrame.
        df = get_zillow_data()
        
        # Write DataFrame to a csv file.
        df.to_csv('zillow_df.csv')
        
    else:
        
        # If csv file exists or cached == True, read in data from csv.
        df = pd.read_csv('zillow_df.csv', index_col=0)
        
    return df





############################# Prepare Zillow ############################# 

# defines function to clean zillow data and return as a cleaned pandas DataFrame
def clean_zillow(df):
    '''
    clean_zillow will take one argument df, a pandas dataframe and will:
    fill in missing values
    replace missing values from total_charges and convert to float
    blah blah blah more cleaning that needs to be done

    return: a single pandas dataframe with the above operations performed
    '''
    
    #fill missing numbers
    df = df.fillna(0)
    
    #replace total_charges missing values and convert to float
    df.total_charges = df.total_charges.str.replace(' ', '0').astype(float)
    

    return df



# splits a dataframe into train, validate, test 
def split(df):
    '''
    take in a DataFrame and return train, validate, and test DataFrames.
    return train, validate, test DataFrames.
    '''
    train_validate, test = train_test_split(df, test_size=.2, random_state=123)
    train, validate = train_test_split(train_validate, 
                                       test_size=.3, 
                                       random_state=123)
    return train, validate, test





# defines MinMaxScaler() and returns scaled data
def min_max_scaler(train, validate, test):
    '''
    Takes in train, validate and test dfs with numeric values only, 
    makes, fits, and uses/transforms the data,
    turns the scaled arrays into dataframes

    Returns (scaler, X_train_scaled, X_validate_scaled, X_test_scaled)
    '''

    #make
    scaler = sklearn.preprocessing.MinMaxScaler()

    #fit
    scaler.fit(train)

    #use
    X_train_scaled = scaler.transform(train)
    X_validate_scaled = scaler.transform(validate)
    X_test_scaled = scaler.transform(test)

    # turn the numpy arrays into dataframes
    X_train_scaled = pd.DataFrame(X_train_scaled, columns=X_train.columns)
    X_validate_scaled = pd.DataFrame(X_validate_scaled, columns=X_train.columns)
    X_test_scaled = pd.DataFrame(X_test_scaled, columns=X_train.columns)


    return scaler, X_train_scaled, X_validate_scaled, X_test_scaled 