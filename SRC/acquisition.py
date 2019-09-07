import pandas as pd
import requests
import os
import json
from functions import state_fixer
from dotenv import load_dotenv
load_dotenv()
census_gov_token = os.getenv("census_gov_token")

#
#
#
# CSV FAST FOOD
# https://www.kaggle.com/datafiniti/fast-food-restaurants/downloads/fast-food-restaurants.zip/3
df_ff = pd.read_csv('../input/fast_food_restaurants.csv')

# Inspect
# print(df_ff.shape)
# print(df_ff.columns)
# print(df_ff.info())

# There is no rows completely duplicate
##duplicate_rows = df_ff.duplicated().sum()
# print(duplicate_rows)

# Some of them seem to be the same register based on the Id and Address
##duplicated_cases = list(df_ff['id'][df_ff['id'].duplicated()].values)
##df_ff_duplicate_cases = df_ff[df_ff['id'].isin(duplicated_cases)]
# display(df_ff_duplicate_cases)

# Therefore I will delete the duplicates that have those two values in common
df_ff = df_ff.drop_duplicates(subset=['id', 'address'])
# df_ff.shape

# Finding if this columns is interesting for my purpose
# print(df_ff.groupby('categories').count()['id'])

# Deleting not useful columns
df_ff = df_ff.drop(['dateAdded', 'country', 'dateUpdated', 'address', 'categories',
                    'keys', 'latitude', 'longitude', 'sourceURLs', 'websites'], axis=1)

# Renaming columns
df_ff.columns = ['id', 'city', 'name', 'postalcode', 'state']

# Check missing values - there is no null values
##null_cols = df_ff.isnull().sum()
# print(null_cols)

# Fixing state column
df_ff['state'] = df_ff['state'].apply(state_fixer)


print(df_ff)

#
#
#
# API INCOME
# https://www.census.gov/data/developers/data-sets/Poverty-Statistics.html


def authRequest(url):
    response = requests.get("{}{}{}".format(url, "&key=", census_gov_token))
    return response.json()


contents = authRequest(
    'https://api.census.gov/data/timeseries/poverty/saipe?get=NAME,SAEMHI_PT,SAEMHI_MOE&for=state:*&time=2017')
df_income = pd.DataFrame(contents)
df_income.columns = df_income.iloc[0]
df_income = df_income.drop(df_income.index[0])
df_income = df_income.drop(['state', 'time', 'SAEMHI_MOE'], axis=1)
df_income.columns = ['state', 'avg_income']
print(df_income)


#
#
#
# API POPULATION
# https://www.census.gov/data/developers/data-sets/popest-popproj.html

contents = authRequest(
    'https://api.census.gov/data/2018/pep/population?get=GEONAME,POP&for=state:*')
df_pop = pd.DataFrame(contents)
df_pop.columns = df_pop.iloc[0]
df_pop = df_pop.drop(df_pop.index[0])
df_pop = df_pop.drop('state', axis=1)
df_pop.columns = ['state', 'population']
print(df_pop)


# GROUP DATA

df_ff_state = df_ff.groupby('state', as_index=True).agg({'name': 'count'})
df_ff_state.columns = ['num_ffrest']

df_ff_state_pop = pd.merge(df_ff_state, df_pop, on='state')
df_ff_state_pop_income = pd.merge(df_ff_state_pop, df_income, on='state')

print(df_ff_state_pop_income)

# Check data types !!!!!!!!!!! NEED TO MODIFY
df_ff_state_pop_income.dtypes
