import numpy as np
import pandas as pd
from clean import df_ff_state_pop_income

# analyze correlation between variables
rs = np.random.RandomState(0)
df = pd.DataFrame(rs.rand(10, 10))
corr = df_ff_state_pop_income.corr()

state_conclusion = "There is a strong negative correlation between the average household income and the number of fast food restaurants per capita in USA States.\nWhere the lower the average household income of the state, the higher the number of fast food restaurants per capita"
