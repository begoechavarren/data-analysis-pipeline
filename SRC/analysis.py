import numpy as np
import pandas as pd
from clean import df_ff_state_pop_income

rs = np.random.RandomState(0)
df = pd.DataFrame(rs.rand(10, 10))
corr = df_ff_state_pop_income.corr()
print(corr)
