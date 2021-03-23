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



# adds caching to get_zillow_data and checks for local filename (zillow_df.csv)
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
    grab the features needed for estimating home value and confirming property location,
    set parcelid as new index,
    rename columns for readability,
    calculate age of home,
    drop null values,
    convert data types to integers, 
    remove outliers from square_feet and tax_value, 
    and calculate tax rate

    return: a single pandas dataframe with the above operations performed
    '''
    
    #select only certain features needed for project
    features = ['parcelid', 
                'bedroomcnt', 
                'bathroomcnt', 
                'calculatedfinishedsquarefeet', 
                'fips', 
                'yearbuilt',
                'taxvaluedollarcnt', 
                'taxamount']

    df = df[features]   
    
    #set parcelid as index
    df = df.set_index("parcelid")

    #rename columns
    df = df.rename(columns={"parcelid": "parcel_id",
                            "bedroomcnt": "bedrooms", 
                            "bathroomcnt": "bathrooms", 
                            "calculatedfinishedsquarefeet":"square_feet", 
                            "fips": "county_fips_code",
                            "taxamount": "taxes",
                            "taxvaluedollarcnt": "tax_value", 
                            "yearbuilt": "age"})
    
    #convert year built to get the property age
    df.age = 2017 - df.age

    #drop the nulls
    df = df.dropna(subset=['square_feet', 'age', 'tax_value', 'taxes'])
    df = df.fillna(0)


    #convert dtypes to integers
    df.bedrooms = df.bedrooms.astype('int64')
    df.square_feet = df.square_feet.astype('int64')
    df.county_fips_code = df.county_fips_code.astype('int64')
    df.age = df.age.astype('int64')
    df.tax_value = df.tax_value.astype('int64')

            
    #remove outliers from square_feet
    #calculate IQR
    q1sf, q3sf = df.square_feet.quantile([.25, .75])
    iqrsf = q3sf - q1sf
            
    #calculate upper and lower bounds, outlier if above or below these
    uppersf = q3sf + (1.5 * iqrsf)
    lowersf = q1sf - (1.5 * iqrsf)
        
    #filter out the lower and upper outliers
    df = df[df.square_feet > lowersf]
    df = df[df.square_feet < uppersf]

    #remove outliers from tax_value
    #calculate IQR
    q1tv, q3tv = df.tax_value.quantile([.25, .75])
    iqrtv = q3tv - q1tv
            
    #calculate upper and lower bounds, outlier if above or below these
    uppertv = q3tv + (1.5 * iqrtv)
    lowertv = q1tv - (1.5 * iqrtv)
        
    #filter out the lower and upper outliers
    df = df[df.tax_value > lowertv]
    df = df[df.tax_value < uppertv]

    #calculate tax rate using property's assessed value and the amount paid each year
                     #tax paid / tax value * 100 = tax rate%
    df['tax_rate'] = (df.taxes / df.tax_value) * 100


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
def Min_Max_Scaler(X_train, X_validate, X_test):
    """
    Takes in X_train, X_validate and X_test dfs with numeric values only
    makes, fits, and uses/transforms the data,
    
    Returns X_train_scaled, X_validate_scaled, X_test_scaled dfs 
    """

    #make and fit
    scaler = sklearn.preprocessing.MinMaxScaler().fit(X_train)

    #use and turn numpy arrays into dataframes
    X_train_scaled = pd.DataFrame(scaler.transform(X_train), index = X_train.index, columns = X_train.columns)
    X_validate_scaled = pd.DataFrame(scaler.transform(X_validate), index = X_validate.index, columns = X_validate.columns)
    X_test_scaled = pd.DataFrame(scaler.transform(X_test), index = X_test.index, columns = X_test.columns)
    
    return X_train_scaled, X_validate_scaled, X_test_scaled