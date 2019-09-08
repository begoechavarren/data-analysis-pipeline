import pandas as pd
from acquisition import df_ff, df_ff_percapita, df_income, df_pop
from functions import state_fixer

# ***********************CSV fast food***********************

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

# ***********************API INCOME***********************

df_income.columns = df_income.iloc[0]
df_income = df_income.drop(df_income.index[0])
df_income = df_income.drop(['state', 'time', 'SAEMHI_MOE'], axis=1)
df_income.columns = ['state', 'avg_income']

# ***********************API POPULATION***********************

df_pop.columns = df_pop.iloc[0]
df_pop = df_pop.drop(df_pop.index[0])
df_pop = df_pop.drop('state', axis=1)
df_pop.columns = ['state', 'population']

# ***********************MERGE DATA***********************

df_ff_state = df_ff.groupby('state', as_index=True).agg({'name': 'count'})
df_ff_state.columns = ['num_ffrest']

df_ff_state_pop = pd.merge(df_ff_state, df_pop, on='state')
df_ff_state_pop_income = pd.merge(df_ff_state_pop, df_income, on='state')

# Modify data types to int64
df_ff_state_pop_income["population"] = df_ff_state_pop_income["population"].astype(
    'int64')
df_ff_state_pop_income["avg_income"] = df_ff_state_pop_income["avg_income"].astype(
    'int64')

# Create new column
df_ff_state_pop_income['ffrest_percapita'] = (
    df_ff_state_pop_income['num_ffrest'] / df_ff_state_pop_income['population'])*10000
df_ff_state_pop_income = df_ff_state_pop_income.drop('num_ffrest', axis=1)

# replace column
df_ff_state_pop_income = df_ff_state_pop_income.drop(
    'ffrest_percapita', axis=1)
df_ff_state_pop_income = pd.merge(
    df_ff_state_pop_income, df_ff_percapita, on='state')
