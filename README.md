# Estimating Home Values 
![Zillow](https://1000logos.net/wp-content/uploads/2017/11/Color-Zillow-Logo.jpg)
****

## About the Project

****

### Goals

[ x ] Develop a regression model that can predict the values of single unit properties using the property data from those with a transaction during May-August 2017 based on the tax assessed value.



[ x ] Confirm where the properties are located.




[ x ] Visualize the distribution of tax rates for each county.

**** 

### Data Dictionary

Feature      | Description   | Data Type
------------ | ------------- | ------------
bedrooms |  Number of bedrooms in home  | int 
bathrooms | Number of bathrooms in home including fractional bathrooms | float
square_feet |  Calculated total finished living area of the home  | int 
county_fips_code |  Federal Information Processing Standard code -  see https://en.wikipedia.org/wiki/FIPS_county_code for more details | int
age |  The difference between the predicting year and the year the principal residence was built  | int
tax_value | The total tax assessed value of the parcel | int
taxes | The total property tax assessed for that assessment year | float
tax_rate | Calculated column by using the property’s assessed value (tax_value) and the taxes paid each year | float

****

### Pipeline Process:

#### Plan
- State project description and goals
- Form hypotheses and brainstorm ideas
- Have all necessary imports ready for project

#### 1. Acquire
- Define functions to:
    - create a sql url using personal credentials
    - get zillow data from MySQL and return as a pandas DataFrame
    - add caching to get_zillow_data to obtain the data quickly
- All functions to acquire the data are included in [wrangle.py](https://github.com/aliciag92/regression-project/blob/main/wrangle.py)
- Complete some initial data summarization and plot distributions of individual variables to get to know data and know what is needed to be prepped/cleaned

#### 2. Prepare
- Define functions to:
    - clean zillow data and return as a cleaned pandas DataFrame
    - split the dataframe into train, validate, test 
    - scale the data
- All functions to prepare the data are included in [wrangle.py](https://github.com/aliciag92/regression-project/blob/main/wrangle.py)

#### 3. Explore
- Address questions posed in planning and brainstorming and figure out drivers to predict home values
- Create visualizations of variables and run statistical tests (as many as needed)
- Summarize key findings and takeaways

#### 4. Model/Evaluate
- Establish and evaluate a baseline model
- Generate various regression algorithms with varying hyperparameters (as many as needed) and settle on the best algorithm by plotting residuals and comparing evaluation metrics.
- Choose the best model and test that final model on out-of-sample data
- Summarize performance, interpret, and document results.

#### 5. Deliver
- Summarization of findings about the drivers of the single unit property values in a [report summary](link to google slides presentation). 


****

### Recreating Project
- To reproduce project, download [wrangle.py](https://github.com/aliciag92/regression-project/blob/main/wrangle.py) and [zillow-report.ipynb](https://github.com/aliciag92/regression-project/blob/main/zillow-report.ipynb) in your working directory and follow the steps from the pipeline process above
- You can always do your own exploring, modeling, and evaluating to deliver any new information.

****
![Zillow](https://1000logos.net/wp-content/uploads/2017/11/Color-Zillow-Logo.jpg)