import pandas as pd
import requests
import os
import json
from dotenv import load_dotenv
load_dotenv()
census_gov_token = os.getenv("census_gov_token")


# CSV FAST FOOD: https://www.kaggle.com/datafiniti/fast-food-restaurants/downloads/fast-food-restaurants.zip/3
df_ff = pd.read_csv('../input/fast_food_restaurants.csv')

# CSV fast food per capita (10K): https://datafiniti.co/fast-food-restaurants-america/
df_ff_percapita = pd.read_csv('../input/ffrest_percapita.csv')

# API INCOME: https://www.census.gov/data/developers/data-sets/Poverty-Statistics.html


def authRequest(url):
    response = requests.get("{}{}{}".format(url, "&key=", census_gov_token))
    return response.json()


contents = authRequest(
    'https://api.census.gov/data/timeseries/poverty/saipe?get=NAME,SAEMHI_PT,SAEMHI_MOE&for=state:*&time=2017')
df_income = pd.DataFrame(contents)

# API POPULATION: https://www.census.gov/data/developers/data-sets/popest-popproj.html

contents = authRequest(
    'https://api.census.gov/data/2018/pep/population?get=GEONAME,POP&for=state:*')
df_pop = pd.DataFrame(contents)
