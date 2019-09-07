import pandas as pd
import requests
import os
import json
from dotenv import load_dotenv
load_dotenv()
census_gov_token = os.getenv("census_gov_token")

#
#
#
# CSV
# https://www.kaggle.com/datafiniti/fast-food-restaurants/downloads/fast-food-restaurants.zip/3
df_fastfood = pd.read_csv('../input/fast_food_restaurants.csv')
print(df_fastfood)

#
#
#
# API
# https://www.census.gov/data/developers/data-sets/Poverty-Statistics.html


def authRequest(url):
    response = requests.get("{}{}{}".format(url, "&key=", census_gov_token))
    return response.json()


contents = authRequest(
    'https://api.census.gov/data/timeseries/poverty/saipe?get=NAME,SAEMHI_PT,SAEMHI_MOE,SAEMHI_PT&for=state:*&time=2017')
df_income = pd.DataFrame(contents)
df_income.columns = df_income.iloc[0]
df_income = df_income.drop(df_income.index[0])
print(df_income)
